# 🤖 AI Restaurant - Smart Food Ordering App

An intelligent food ordering application powered by Large Language Models (LLMs) that understands natural language orders and provides real-time availability checking with smart suggestions.

## 🌟 Features

- **Natural Language Processing**: Customers can order food using conversational language
- **AI-Powered Availability Checking**: LLM determines if items are available and suggests alternatives
- **Real-Time Menu Display**: Browse the full menu with live availability status
- **Smart Suggestions**: AI recommends similar items when requested items are unavailable
- **Modern UI/UX**: Beautiful, responsive design with smooth animations
- **Fallback System**: Works even when AI services are unavailable
- **Mobile-Friendly**: Fully responsive design for all devices

## 🏗️ Architecture

- **Backend**: Python Flask with RESTful API
- **Frontend**: Vanilla JavaScript with modern ES6+ features
- **AI Integration**: OpenAI GPT-3.5-turbo (easily configurable for other LLMs)
- **Styling**: Modern CSS with animations and responsive design
- **Data**: In-memory menu storage (easily extensible to databases)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key (or other LLM provider)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-restaurant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

## 🎯 How It Works

### Order Processing Flow

1. **Customer Input**: User types their order in natural language
2. **AI Analysis**: LLM processes the order against the current menu
3. **Availability Check**: System checks real-time inventory
4. **Response Generation**: AI generates friendly response with:
   - Available items and total price
   - Unavailable items with alternatives
   - Helpful suggestions

### Example Orders

Try these example orders:
- "I'd like a burger and some wings, also a coke please"
- "Can I get the salmon with a side salad?"
- "Do you have any vegetarian options?"
- "I want pizza and wine for dinner"

## 🔧 Configuration

### LLM Provider

The app uses OpenAI by default, but you can easily switch to other providers:

```python
# For Anthropic Claude
import anthropic
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# For Cohere
import cohere
co = cohere.Client(os.getenv('COHERE_API_KEY'))
```

### Menu Customization

Edit the `RESTAURANT_MENU` dictionary in `app.py`:

```python
RESTAURANT_MENU = {
    "category_name": [
        {
            "name": "Item Name",
            "price": 12.99,
            "available": True,
            "description": "Item description"
        }
    ]
}
```

## 📱 API Endpoints

- `GET /` - Main application page
- `GET /menu` - Get full menu with availability
- `POST /order` - Process order with AI
- `GET /health` - Health check endpoint

### Order API Example

```bash
curl -X POST http://localhost:5000/order \
  -H "Content-Type: application/json" \
  -d '{"order": "I want a burger and fries"}'
```

## 🎨 UI Components

### Order Section
- Natural language input textarea
- AI processing indicator
- Status badges (Available/Partially Available/Unavailable)
- Items found with pricing
- Alternative suggestions

### Menu Section
- Categorized menu display
- Real-time availability indicators
- Scrollable interface
- Item descriptions and pricing

## 🔒 Security Features

- Input validation and sanitization
- CORS protection
- Error handling with graceful fallbacks
- Environment variable protection

## 🚢 Deployment

### Local Development
```bash
python app.py
```

### Production with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🧪 Testing

The app includes comprehensive error handling and fallback mechanisms:

- **AI Service Unavailable**: Falls back to keyword matching
- **Network Issues**: Graceful error messages
- **Invalid Input**: User-friendly validation
- **Menu Loading Errors**: Fallback display

## 🔮 Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication and order history
- [ ] Payment processing integration
- [ ] Real-time inventory management
- [ ] Multi-language support
- [ ] Voice ordering capability
- [ ] Order tracking and notifications
- [ ] Restaurant admin dashboard
- [ ] Analytics and reporting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙋‍♂️ Support

For questions or issues:
- Create an issue in the repository
- Check the troubleshooting section below

## 🔧 Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **AI responses not working**
   - Check your OpenAI API key in `.env`
   - Verify API key has sufficient credits
   - Check network connectivity

3. **Port already in use**
   - Change port in `app.py`: `app.run(port=5001)`
   - Or kill existing process: `lsof -ti:5000 | xargs kill`

4. **Styling not loading**
   - Clear browser cache
   - Check console for 404 errors
   - Verify static file paths

---

**Built with ❤️ using Flask, OpenAI, and modern web technologies**
