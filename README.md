# Smart-City-Backend

Smart-City-Backend is a powerful backend solution designed to integrate smart systems for managing accommodations like hotels and auberges. It leverages the Django framework for building the backend and integrates AI-powered recommendation systems using Optuna to provide personalized packages for users.

## Technologies Used 
- Python 3.10.11
- Django 5.0.7
- Django rest framework 3.15.2
- Django rest framework simplejwt 5.3.1
- SQLite 

## Features

- **Accommodation Management:**
  - Hotels: Manage hotel details, offers, and cover images.
  - Auberges: Manage auberge details, offers, and associated images.
- **AI-Powered Package Recommendation:**
  - Suggests the best accommodation packages based on user-defined budgets and stay durations.
  - Utilizes Optuna for optimizing recommendations.
- **Combined Results:**
  - Combines results from both hotels and auberges for comprehensive user options.
- **Customizable Search Filters:**
  - Adjust budget and duration ranges dynamically via query parameters.

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

## API Endpoints

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
        # ... implementation as discussed ...
        return Response(response_data)
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
