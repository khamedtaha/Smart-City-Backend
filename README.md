# Smart-City-Backend

Smart-City-Backend is a robust backend solution designed to integrate smart systems for managing various types of accommodations like hotels, auberges, and hauberges. The system leverages the Django framework for building the backend and integrates AI-powered recommendation systems using Optuna to provide personalized packages for users based on their preferences .

## Technologies Used 
- Python 3.10.11
- Django 5.0.7
- Django rest framework 3.15.2
- Django Rest Framework SimpleJWT 5.3.1
- SQLite 
- Gemini Pro API (for advanced AI-powered features)
- Optuna (for hyperparameter optimization and recommendation systems)

## API Docs 
- [https://smartcity.zsp-dz.com/api/docs/](https://smartcity.zsp-dz.com/api/docs/)

## Base Dashboard 
- [https://smartcity.zsp-dz.com/dash/](https://smartcity.zsp-dz.com/dash/)
  
  **Username :** `SmartAdmin`  
  **Password :** `SmartAdmin@password`

## Features
- **Management **
- **Accommodation Management :**
  - Hotels: Manage hotel details, offers, and cover images .
  - Auberges: Manage auberge details, offers, and associated images .
  - Hauberge Management .
  - Hotel integration .
  - Places Management . 
  - Resident Mangment . 
  - Event integration .
- **AI-Powered Package Recommendation :**
  - Suggests the best accommodation packages based on user-defined budgets and stay durations .
  - Utilizes Optuna for optimizing recommendations.
- **Combined Results :**
  - Combines results from both hotels and auberges for comprehensive user options .
- **Customizable Search Filters :**
  - Adjust budget and duration ranges dynamically via query parameters .
- **External API Integration :**
  - Leverage external APIs for enhanced data aggregation, such as fetching additional tourist attraction details .
- **Real-Time Language Support :**
  - Provide responses in multiple languages (English, French, and Arabic) based on user preferences.
- **Hotel Integration**
   - **Data Synchronization** : Integrate hotel data and functionalities into the broader platform for a consistent user experience across various accommodation types.
   
- **Places Management**
   - **Location Categorization** : Manage the addition, modification, and categorization of various places, enhancing the tourism experience by allowing users to explore and select locations conveniently.

- **Resident Management**
   - **Long-term Resident Profiles** : Manage resident details, preferences, and communication for personalized services to enhance long-term stays.
   - **Preference Tracking** : Customize services based on resident preferences to improve customer satisfaction.

- **Event Integration**
   - **Local Event Linkage** : Link local events with accommodations, offering combined packages for users looking to book stays along with event tickets.
   - **Enhanced User Experience** : Ensure that users can seamlessly plan their visits by providing both accommodation and event options in one platform.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Smart-City-Backend.git
   cd Smart-City-Backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Run the server:
   ```bash
   python manage.py runserver
   ```

## Example API Endpoint 
 - Exist More Api read docs api 

### Suggest Package API
**Endpoint:** `/suggest-package/`

**Method:** `GET`

**Query Parameters:**
- `min_budget` (default: 50): Minimum budget for the package.
- `max_budget` (default: 500): Maximum budget for the package.
- `min_days` (default: 1): Minimum number of days for the stay.
- `max_days` (default: 10): Maximum number of days for the stay.

**Response:**
- `best_budget`: Optimized budget.
- `best_days`: Optimized number of days.
- `optimized_offres`: A list of recommended packages divided into hotels and auberges.

### Example Request
```bash
GET /suggest-package/?min_budget=100&max_budget=300&min_days=2&max_days=7
```

**Example Response:**
```json
{
    "best_budget": 200,
    "best_days": 5,
    "optimized_offres": {
        "hotels": [
            {
                "id": 1,
                "offer_name": "Deluxe Room",
                "prix": 180,
                "location_name": "Luxury Hotel"
            }
        ],
        "auberges": [
            {
                "id": 2,
                "offer_name": "Camp Tent",
                "prix": 150,
                "location_name": "Desert Camp"
            }
        ]
    }
}
```

## Models

### Hotel
```python
class Hotel(models.Model):
    TYPE_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    nom = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    type = models.IntegerField(choices=TYPE_CHOICES)
    web_site = models.URLField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='hotel_covers/', blank=True, null=True)
    location = PlainLocationField(blank=True)

    def __str__(self):
        return self.nom
```

### Auberge
```python
class Hauberge(models.Model):
    TYPE_CHOICES = [
        ('maison', 'Maison'),
        ('camp', 'Camp'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    capacite = models.IntegerField()
    nom = models.CharField(max_length=255)
    emplacement = PlainLocationField(blank=True)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    disponibilite = models.BooleanField(default=True)

    def __str__(self):
        return self.nom
```

### Package Optimization
```python
class SuggestPackageView(APIView):
   def get(self, request):
      hotel_offres = HotelOffre.objects.filter(is_base=True).values("id", "name", "prix", "hotel__nom")
      hauberge_offres = HaubergeOffre.objects.all().values("id", "titre", "prix", "hauberge__nom")

      hotel_df = pd.DataFrame(list(hotel_offres))
      hauberge_df = pd.DataFrame(list(hauberge_offres))

      hotel_df.rename(columns={"hotel__nom": "location_name", "name": "offer_name", "prix": "price"}, inplace=True)
      hauberge_df.rename(columns={"hauberge__nom": "location_name", "titre": "offer_name", "prix": "price"}, inplace=True)

      hotel_df['type'] = 'hotel'
      hauberge_df['type'] = 'hauberge'

      combined_df = pd.concat([hotel_df, hauberge_df], ignore_index=True)
      combined_df = combined_df.dropna(subset=['price'])

      min_budget = int(request.query_params.get("min_budget", 50))
      max_budget = int(request.query_params.get("max_budget", 500))
      min_days = int(request.query_params.get("min_days", 1))
      max_days = int(request.query_params.get("max_days", 10))

      def objective(trial):
            budget = trial.suggest_int("budget", min_budget, max_budget)  
            days = trial.suggest_int("days", min_days, max_days)

            filtered_df = combined_df[combined_df['price'] <= budget]
            if filtered_df.empty:
               return float('inf')

            return min(filtered_df['price']) * days

      study = optuna.create_study(direction="minimize")
      study.optimize(objective, n_trials=20)

      
      best_budget = study.best_params['budget']
      best_days = study.best_params['days']
      final_offres = combined_df[combined_df['price'] <= best_budget]

      hotel_results = final_offres[final_offres['type'] == 'hotel'].to_dict(orient="records")
      hauberge_results = final_offres[final_offres['type'] == 'hauberge'].to_dict(orient="records")

      return Response({
            "best_budget": best_budget,
            "best_days": best_days,
            "hotels": hotel_results,
            "hauberges": hauberge_results
      })
```

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push the branch and create a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or inquiries, contact [Your Name](mailto:your-email@example.com).
