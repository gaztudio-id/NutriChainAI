import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from itertools import islice
from youtube_comment_downloader import YoutubeCommentDownloader
import motor.motor_asyncio
from datetime import datetime, timedelta
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
app = FastAPI(title="Makan Bergizi Gratis - ML Service")
mongo_client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db = mongo_client['mbg_database']
sentiment_collection = db['sentiments']
try:
    bert_path = "./Model-Bert"
    tokenizer = AutoTokenizer.from_pretrained(bert_path)
    model = AutoModelForSequenceClassification.from_pretrained(bert_path)
    sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    print("BERT model loaded successfully.")
except Exception as e:
    print(f"Error loading BERT model: {e}")
    sentiment_pipeline = None
try:
    lstm_path = "./Model-Forecasting/model_lstm_sentimen.h5"
    lstm_model = tf.keras.models.load_model(lstm_path, compile=False)
    print("LSTM model loaded successfully.")
except Exception as e:
    print(f"Error loading LSTM model: {e}")
    lstm_model = None
class SentimentRequest(BaseModel):
    text: str
class SentimentResponse(BaseModel):
    label: str
    score: float
class ForecastRequest(BaseModel):
    sequence: List[float] 
class ForecastResponse(BaseModel):
    prediction: List[float]
class ScrapeRequest(BaseModel):
    url: str
    max_comments: int = 50
class CommentSentiment(BaseModel):
    text: str
    label: str
    score: float
class ScrapeResponse(BaseModel):
    total_comments: int
    positive: int
    negative: int
    comments: List[CommentSentiment]
@app.post("/api/sentiment", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    if not sentiment_pipeline:
        raise HTTPException(status_code=500, detail="Sentiment model not loaded.")
    try:
        short_text = request.text[:500]
        result = sentiment_pipeline(short_text)[0]
        label = result['label']
        if label.lower() == 'positive' or 'positif' in label.lower() or label == 'LABEL_2' or label == 'LABEL_1':
            label_str = 'Positif'
        elif label.lower() == 'negative' or 'negatif' in label.lower() or label == 'LABEL_0':
            label_str = 'Negatif'
        else:
            label_str = label
        sentiment_doc = {
            "text": request.text,
            "label": label_str,
            "score": float(result['score']),
            "created_at": datetime.utcnow()
        }
        await sentiment_collection.insert_one(sentiment_doc)
        return SentimentResponse(label=label_str, score=result['score'])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.get("/api/sentiment-trends")
async def get_sentiment_trends():
    try:
        current_year = datetime.utcnow().year
        start_date = datetime(current_year, 1, 1)
        end_date = datetime(current_year + 1, 1, 1)
        pipeline = [
            {
                "$match": {
                    "created_at": {
                        "$gte": start_date,
                        "$lt": end_date
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$created_at"},
                        "month": {"$month": "$created_at"}
                    },
                    "positive": {
                        "$sum": {"$cond": [{"$eq": ["$label", "Positif"]}, 1, 0]}
                    },
                    "negative": {
                        "$sum": {"$cond": [{"$eq": ["$label", "Negatif"]}, 1, 0]}
                    }
                }
            },
            {
                "$sort": {"_id.year": 1, "_id.month": 1}
            }
        ]
        cursor = sentiment_collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        trends = []
        for res in results:
            if not res['_id'].get('year') or not res['_id'].get('month'):
                continue
            month_str = f"{res['_id']['year']}-{str(res['_id']['month']).zfill(2)}"
            trends.append({
                "month": month_str,
                "positive": res['positive'],
                "negative": res['negative']
            })
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch trends: {str(e)}")
@app.get("/api/forecast")
async def generate_forecast():
    if not lstm_model:
        raise HTTPException(status_code=500, detail="Forecasting model not loaded.")
    try:
        cursor = sentiment_collection.find({})
        results = await cursor.to_list(length=None)
        if not results:
            raise HTTPException(status_code=400, detail="No data available for forecasting.")
        df = pd.DataFrame(results)
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['date'] = df['created_at'].dt.date
        daily_agg = df.groupby('date').agg(
            total=('label', 'count'),
            positif=('label', lambda x: (x == 'Positif').sum())
        )
        daily_agg.index = pd.to_datetime(daily_agg.index)
        today = pd.to_datetime('today').normalize()
        min_date = daily_agg.index.min()
        max_date = max(daily_agg.index.max(), today)
        full_date_range = pd.date_range(start=min_date, end=max_date, freq='D')
        daily_agg = daily_agg.reindex(full_date_range)
        daily_agg['total'] = daily_agg['total'].fillna(0)
        daily_agg['positif'] = daily_agg['positif'].fillna(0)
        daily_agg = daily_agg.reset_index().rename(columns={'index': 'date'})
        daily_agg['rasio_positif'] = daily_agg['positif'] / daily_agg['total']
        daily_agg['rasio_positif'] = daily_agg['rasio_positif'].replace([np.inf, -np.inf], np.nan)
        daily_agg['rasio_positif'] = daily_agg['rasio_positif'].ffill().fillna(0.5)
        daily_agg['rasio_smooth'] = daily_agg['rasio_positif'].rolling(window=7, min_periods=1).mean()
        LOOK_BACK = 14
        if len(daily_agg) < LOOK_BACK:
            raise HTTPException(status_code=400, detail=f"Not enough data. Need at least {LOOK_BACK} days.")
        scaler_daily = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler_daily.fit_transform(daily_agg[['rasio_smooth']].values)
        last_sequence = scaled_data[-LOOK_BACK:]
        current_input = last_sequence.reshape((1, LOOK_BACK, 1))
        future_days = 30
        predictions_scaled = []
        for _ in range(future_days):
            pred = lstm_model.predict(current_input, verbose=0)
            predictions_scaled.append(pred[0, 0])
            pred_reshaped = np.array([[[pred[0, 0]]]])
            current_input = np.append(current_input[:, 1:, :], pred_reshaped, axis=1)
        predictions = scaler_daily.inverse_transform(np.array(predictions_scaled).reshape(-1, 1)).flatten()
        last_date = pd.to_datetime(daily_agg['date'].iloc[-1])
        history = []
        hist_df = daily_agg.tail(60)
        for _, row in hist_df.iterrows():
            history.append({
                "date": row['date'].strftime('%Y-%m-%d'),
                "value": row['rasio_smooth']
            })
        forecast = []
        for i in range(1, future_days + 1):
            next_date = last_date + timedelta(days=i)
            forecast.append({
                "date": next_date.strftime('%Y-%m-%d'),
                "value": float(predictions[i-1])
            })
        return {
            "history": history,
            "forecast": forecast
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))
@app.post("/api/scrape", response_model=ScrapeResponse)
async def scrape_and_analyze(request: ScrapeRequest):
    if not sentiment_pipeline:
        raise HTTPException(status_code=500, detail="Sentiment model not loaded.")
    try:
        downloader = YoutubeCommentDownloader()
        generator = downloader.get_comments_from_url(request.url, sort_by=0) 
        comments_data = []
        pos_count = 0
        neg_count = 0
        for comment in islice(generator, request.max_comments):
            text = comment['text']
            if not text.strip():
                continue
            short_text = text[:500]
            try:
                result = sentiment_pipeline(short_text)[0]
                label = result['label']
                score = result['score']
                if label.lower() == 'positive' or 'positif' in label.lower() or label == 'LABEL_2' or label == 'LABEL_1':
                    pos_count += 1
                    label_str = 'Positif'
                elif label.lower() == 'negative' or 'negatif' in label.lower() or label == 'LABEL_0':
                    neg_count += 1
                    label_str = 'Negatif'
                else:
                    continue
                comments_data.append(CommentSentiment(
                    text=text,
                    label=label_str,
                    score=score
                ))
            except Exception as e:
                pass
        return ScrapeResponse(
            total_comments=len(comments_data),
            positive=pos_count,
            negative=neg_count,
            comments=comments_data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to scrape or analyze: {str(e)}")
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
async def serve_index():
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not found. Please create static/index.html"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)