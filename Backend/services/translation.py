from transformers import MarianMTModel, MarianTokenizer
from typing import Optional

# Predefined translation mappings
TRANSLATION_MODELS = {
    ('en', 'es'): 'Helsinki-NLP/opus-mt-en-es',
    ('en', 'fr'): 'Helsinki-NLP/opus-mt-en-fr',
    ('en', 'de'): 'Helsinki-NLP/opus-mt-en-de',
    ('es', 'en'): 'Helsinki-NLP/opus-mt-es-en',
    ('fr', 'en'): 'Helsinki-NLP/opus-mt-fr-en',
    ('de', 'en'): 'Helsinki-NLP/opus-mt-de-en',
}

def translate_text(text: str, src_lang: str = "en", tgt_lang: str = "es") -> Optional[str]:
    """
    Translate text between supported languages.
    
    Args:
        text (str): Text to translate
        src_lang (str): Source language code
        tgt_lang (str): Target language code
    
    Returns:
        Optional[str]: Translated text or None if translation fails
    """
    if not text:
        return None

    # Normalize language codes
    src_lang = src_lang.lower()
    tgt_lang = tgt_lang.lower()

    # Check if a direct translation model exists
    model_key = (src_lang, tgt_lang)
    if model_key not in TRANSLATION_MODELS:
        # Try translating via English as an intermediate language
        intermediate_models = [
            (src_lang, 'en'),
            ('en', tgt_lang)
        ]
        
        # First translate to English
        intermediate_text = text
        for inter_src, inter_tgt in intermediate_models:
            if (inter_src, inter_tgt) in TRANSLATION_MODELS:
                try:
                    model_name = TRANSLATION_MODELS[(inter_src, inter_tgt)]
                    tokenizer = MarianTokenizer.from_pretrained(model_name)
                    model = MarianMTModel.from_pretrained(model_name)
                    
                    inputs = tokenizer(intermediate_text, return_tensors="pt", padding=True)
                    translated = model.generate(**inputs)
                    intermediate_text = tokenizer.decode(translated[0], skip_special_tokens=True)
                except Exception as e:
                    print(f"Translation error: {e}")
                    return None
            else:
                return None

        return intermediate_text

    try:
        model_name = TRANSLATION_MODELS[model_key]
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        
        inputs = tokenizer(text, return_tensors="pt", padding=True)
        translated = model.generate(**inputs)
        return tokenizer.decode(translated[0], skip_special_tokens=True)
    
    except Exception as e:
        print(f"Translation error: {e}")
        return None
