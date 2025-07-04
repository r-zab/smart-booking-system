import pandas as pd
from sklearn.linear_model import LinearRegression
from .models import Booking
from datetime import date, timedelta

def prepare_booking_data():
    bookings = Booking.objects.all()

    if not bookings.exists():
        return pd.DataFrame()

    start_times = [b.start_time for b in bookings]

    df = pd.DataFrame(start_times, columns=['start_time'])

    df['booking_date'] = pd.to_datetime(df['start_time']).dt.date
    daily_counts = df.groupby('booking_date').size().reset_index(name='booking_count')
    daily_counts['day_of_year'] = pd.to_datetime(daily_counts['booking_date']).dt.dayofyear

    return daily_counts

def train_prediction_model(df):
    if df.empty or len(df) < 2:
        return None

    X = df[['day_of_year']]
    y = df['booking_count']

    model = LinearRegression()
    model.fit(X, y)

    return model

def get_future_predictions(model, days_to_predict=7):
    if model is None:
        return {}

    today = date.today()
    predictions = {}

    for i in range(days_to_predict):
        future_date = today + timedelta(days=i + 1)
        future_day_of_year = pd.to_datetime(future_date).dayofyear

        predicted_count = model.predict([[future_day_of_year]])

        predictions[future_date.strftime('%Y-%m-%d')] = round(max(0, predicted_count[0]))

    return predictions
