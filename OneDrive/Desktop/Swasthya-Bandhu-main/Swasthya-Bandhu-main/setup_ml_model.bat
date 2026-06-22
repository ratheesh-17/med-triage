@echo off
echo 🏥 Medical AI Model Setup Script
echo ================================

echo.
echo 📦 Installing ML dependencies...
cd ml_models
pip install -r requirements.txt

echo.
echo 📊 Collecting and preparing training data...
python data_collection.py

echo.
echo 🤖 Training the medical AI model...
python train_model.py

echo.
echo ✅ Setup completed!
echo.
echo 📋 Next steps:
echo 1. Update your backend to use the custom AI service
echo 2. Test the integration
echo 3. Monitor model performance

pause