from django.shortcuts import render
import os
import pickle
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.admin.views.decorators import staff_member_required
import numpy as np
import pandas as pd


@staff_member_required
def forecast_dashboard(request):
    # Default forecast period
    forecast_period = 7

    # Check if a forecast period was selected
    if request.method == 'POST':
        forecast_period = int(request.POST.get('forecast_period', 7))

    # Generate forecast data
    forecast_data = generate_forecast(forecast_period)

    # Available forecast periods for dropdown
    forecast_periods = [
        (7, '7 days'),
        (30, '1 month'),
        (180, '6 months'),
        (360, '1 year'),
    ]

    context = {

        'forecast_period': forecast_period,
        'forecast_periods': forecast_periods,
        'forecast_data': forecast_data,
    }
    return render(request, 'admin/forecast/forecast_dashboard.html', context)


def generate_forecast(period):
    # Paths to the saved models
    shoe_model_path = os.path.join(settings.BASE_DIR, 'forecast', 'models', 'shoe_sales_model.pkl')
    panjabi_model_path = os.path.join(settings.BASE_DIR, 'forecast', 'models', 'panjabi_sales_model.pkl')
    attar_model_path = os.path.join(settings.BASE_DIR, 'forecast', 'models', 'attar_sales_model.pkl')

    # Define Eid periods (for future predictions)
    eid_periods = [
        (datetime(2024, 3, 29), datetime(2024, 4, 9)),  # Eid al-Fitr 2024
        (datetime(2024, 6, 9), datetime(2024, 6, 16)),  # Eid al-Adha 2024
        (datetime(2025, 3, 18), datetime(2025, 3, 29)),  # Eid al-Fitr 2025
        (datetime(2025, 5, 29), datetime(2025, 6, 5))  # Eid al-Adha 2025
    ]

    try:
        # Load all three pre-trained models
        with open(shoe_model_path, 'rb') as f:
            shoe_model = pickle.load(f)

        with open(panjabi_model_path, 'rb') as f:
            panjabi_model = pickle.load(f)

        with open(attar_model_path, 'rb') as f:
            attar_model = pickle.load(f)

        # Generate forecasts for all three models
        results = {}
        total_sales = {}

        for model_name, model in [('Shoes', shoe_model), ('Panjabi', panjabi_model), ('Attar', attar_model)]:
            # Create a future dataframe
            future = model.make_future_dataframe(periods=period)

            # Add the 'is_eid' column to the future dataframe
            is_eid_future = np.zeros(len(future))
            for i, row in future.iterrows():
                date = row['ds']
                for start_date, end_date in eid_periods:
                    if start_date <= date <= end_date:
                        is_eid_future[i] = 1
                        break
            future['is_eid'] = is_eid_future

            # Generate the forecast
            forecast = model.predict(future)

            # Get the last historical date from the training data
            last_date = model.history['ds'].max()

            # Filter for future dates only
            future_forecast = forecast[forecast['ds'] > last_date]

            # Save the forecast data
            forecast_dates = future_forecast['ds'].dt.strftime('%Y-%m-%d').tolist()
            forecast_values = future_forecast['yhat'].tolist()

            # Calculate total sales for this category
            total_sales[model_name] = round(future_forecast['yhat'].sum())

            results[model_name] = {
                'dates': forecast_dates,
                'values': forecast_values
            }

        # Calculate percentages for pie chart
        total_sum = sum(total_sales.values())
        percentages = {k: (v / total_sum) * 100 for k, v in total_sales.items()}

        return {
            'categories': list(results.keys()),
            'dates': results['Shoes']['dates'],  # All models have the same dates
            'shoe_values': results['Shoes']['values'],
            'panjabi_values': results['Panjabi']['values'],
            'attar_values': results['Attar']['values'],
            'pie_labels': list(total_sales.keys()),
            'pie_values': list(total_sales.values()),
            'pie_percentages': [round(p, 1) for p in percentages.values()]
        }

    except Exception as e:
        # Handle error (model file not found, etc.)
        print(f"Error loading models or generating forecast: {e}")

        # Return placeholder data
        start_date = datetime.now()
        dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(period)]
        placeholder_values = [0] * period

        return {
            'categories': ['Shoes', 'Panjabi', 'Attar'],
            'dates': dates,
            'shoe_values': placeholder_values,
            'panjabi_values': placeholder_values,
            'attar_values': placeholder_values,
            'pie_labels': ['Shoes', 'Panjabi', 'Attar'],
            'pie_values': [0, 0, 0],
            'pie_percentages': [33.3, 33.3, 33.4],
            'error': str(e)
        }
