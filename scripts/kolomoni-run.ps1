Write-Output "Starting Stari Kolomoni API (uvicorn main:app)..."
poetry run uvicorn main:app --reload
