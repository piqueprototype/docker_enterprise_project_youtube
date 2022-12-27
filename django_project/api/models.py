from django.db import models

# Create your models here.
class Weather(models.Model):
    """ Weather model """
    id = models.BigAutoField(db_column="Weather ID", primary_key=True, unique=True, null=False, editable=False, verbose_name="Weather ID")
    type = models.CharField(max_length=25, db_column="Weather Type", verbose_name="Weather Type")
    description = models.CharField(max_length=30, db_column="Weather Description", verbose_name="Weather Description")
    temperature = models.FloatField(db_column="Temperature (Kelvin)", verbose_name="Temperature (Kelvin)")
    feels_like = models.FloatField(db_column="Temperature (Feels Like)", verbose_name="Temperature (Feels Like)")
    temp_min = models.FloatField(db_column="Temperature (Minimum)", verbose_name="Temperature (Minimum)")
    temp_max = models.FloatField(db_column="Temperature (Maximum)", verbose_name="Temperature (Maximum)")
    pressure = models.PositiveIntegerField(db_column="Atmospheric Pressure", verbose_name="Atmospheric Pressure")
    humidity = models.PositiveSmallIntegerField(db_column="Humidity", verbose_name="Humidity")
    sea_level_pressure = models.PositiveIntegerField(db_column="Sea Level Pressure", verbose_name="Sea Level Pressure")
    ground_level_press = models.PositiveIntegerField(db_column="Ground Level Pressure", verbose_name="Ground Level Pressure")
    visibility = models.PositiveIntegerField(db_column="Visibility", verbose_name="Visibility")
    wind_speed = models.FloatField(db_column="Wind Speed", verbose_name="Wind Speed")
    wind_degree = models.PositiveSmallIntegerField(db_column="Wind Degree", verbose_name="Wind Degree")
    wind_gust = models.FloatField(db_column="Wind Gust", verbose_name="Wind Gust")
    rain_volume = models.FloatField(db_column="Rain Volume", verbose_name="Rain Volume")
    snow_volume = models.FloatField(db_column="Snow Volume", verbose_name="Snow Volume")
    cloud_percent = models.PositiveSmallIntegerField(db_column="Cloud Percentage", verbose_name="Cloud Percentage")
    collected_unix_time = models.PositiveBigIntegerField(db_column="UNIX timestamp", unique=True, verbose_name="UNIX timestamp")
    sunrise = models.PositiveBigIntegerField(db_column="Sunrise", verbose_name="Sunrise")
    sunset = models.PositiveBigIntegerField(db_column="Sunset", verbose_name="Sunset")
    city = models.CharField(max_length=35, db_column="City Name", verbose_name="City Name")
