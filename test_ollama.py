#!/usr/bin/env python3

import ollama
import json

def test_ollama():
    try:
        print("🔍 Test connessione Ollama...")
        
        # Test 1: Lista modelli
        models = ollama.list()
        print(f"✅ Modelli disponibili: {models}")
        
        # Test 2: Generazione semplice
        print("\n🔍 Test generazione semplice...")
        simple_response = ollama.generate(
            model='gemma3:4b-it-qat',
            prompt='Ciao, rispondi con "OK"',
            stream=False
        )
        print(f"Risposta semplice: {simple_response}")
        
        # Test 3: Generazione JSON
        print("\n🔍 Test generazione JSON...")
        json_prompt = 'Rispondi solo con questo JSON: [{"test": "valore"}]'
        json_response = ollama.generate(
            model='gemma3:4b-it-qat',
            prompt=json_prompt,
            stream=False,
            options={
                "temperature": 0.1,
                "top_p": 0.3,
                "num_predict": 100
            }
        )
        print(f"Risposta JSON completa: {json_response}")
        print(f"Solo response field: {json_response.get('response', 'MISSING')}")
        
        # Test 4: Con più opzioni
        print("\n🔍 Test con opzioni complete...")
        full_response = ollama.generate(
            model='gemma3:4b-it-qat',
            prompt='Crea una flashcard: {"domanda": "Che cos\'è Python?", "risposta": "Un linguaggio di programmazione", "tipo": "aperta", "punteggio": 2}',
            stream=False,
            options={
                "temperature": 0.1,
                "top_p": 0.3,
                "num_predict": 200,
                "stop": ["```", "END"]
            }
        )
        print(f"Risposta completa: {full_response}")
        
    except Exception as e:
        print(f"❌ Errore: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ollama() 