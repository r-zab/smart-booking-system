import pandas as pd
from sklearn.linear_model import LinearRegression
from .models import Booking
from datetime import date, timedelta

# booking/analysis.py

def prepare_booking_data():
    """
    Pobiera wszystkie rezerwacje z bazy danych i agreguje je,
    licząc liczbę rezerwacji na każdy dzień.
    Zwraca dane w formacie pandas DataFrame.
    """
    # Pobieramy całe obiekty rezerwacji
    bookings = Booking.objects.all()

    # Sprawdzamy, czy w ogóle istnieją jakieś rezerwacje
    if not bookings.exists():
        return pd.DataFrame()

    # Ręcznie tworzymy listę dat rozpoczęcia z obiektów
    start_times = [b.start_time for b in bookings]

    # Tworzymy DataFrame, jawnie podając nazwę dla naszej kolumny
    df = pd.DataFrame(start_times, columns=['start_time'])

    # Reszta funkcji pozostaje bez zmian
    df['booking_date'] = pd.to_datetime(df['start_time']).dt.date
    daily_counts = df.groupby('booking_date').size().reset_index(name='booking_count')
    daily_counts['day_of_year'] = pd.to_datetime(daily_counts['booking_date']).dt.dayofyear

    return daily_counts

def train_prediction_model(df):
    """
    Trenuje prosty model regresji liniowej na podstawie danych o rezerwacjach.
    """
    if df.empty or len(df) < 2:
        return None # Nie można trenować modelu na zbyt małej ilości danych

    # Nasza cecha (na podstawie czego przewidujemy) to dzień roku
    X = df[['day_of_year']]
    # Nasz cel (to, co chcemy przewidzieć) to liczba rezerwacji
    y = df['booking_count']

    # Tworzymy i trenujemy model
    model = LinearRegression()
    model.fit(X, y)

    return model

def get_future_predictions(model, days_to_predict=7):
    """
    Używa wytrenowanego modelu do przewidywania liczby rezerwacji
    na następne 'days_to_predict' dni.
    """
    if model is None:
        return {}

    today = date.today()
    predictions = {}

    for i in range(days_to_predict):
        # Bierzemy dzień w przyszłości
        future_date = today + timedelta(days=i + 1)
        # Konwertujemy go na tę samą cechę, na której trenowaliśmy model (dzień roku)
        future_day_of_year = pd.to_datetime(future_date).dayofyear

        # Model przewiduje liczbę rezerwacji
        predicted_count = model.predict([[future_day_of_year]])

        # Zapisujemy wynik w formacie 'YYYY-MM-DD': prognoza
        # Używamy max(0, ...) aby nie mieć ujemnych rezerwacji
        predictions[future_date.strftime('%Y-%m-%d')] = round(max(0, predicted_count[0]))

    return predictions