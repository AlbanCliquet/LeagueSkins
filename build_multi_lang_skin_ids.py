"""
Build skin ID to name mapping for all available languages from CommunityDragon.

This script fetches champion data from CommunityDragon API for each language
and creates a skin_ids.json file mapping skin IDs to their localized names.

Output: resources/skinid_mapping/{lang_code}/skin_ids.json
"""

import requests
import json
import re
from pathlib import Path
from typing import List, Dict, Optional

# Community Dragon API base URLs
CDRAGON_BASE_URL = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global"

# Languages from CommunityDragon
# Note: All en_X variants use the same mapping as "default" (which is en_US)
# We'll process only one locale per language code
LANGUAGES = [
    "ar_ae", "cs_cz", "de_de", "default", "el_gr", "en_gb", 
    "es_es", "fr_fr", "hu_hu", "id_id", "it_it", 
    "ja_jp", "ko_kr", "pl_pl", "pt_br", "ro_ro", "ru_ru", "th_th", "tr_tr", 
    "vi_vn", "zh_cn", "zh_tw"
]

# Map language codes to their primary locale (first ll_ll format)
# All en_X variants (en_au, en_gb, en_ph, en_sg) map to "default" (en_US)
LANGUAGE_TO_LOCALE = {
    "ar": "ar_ae",
    "cs": "cs_cz", 
    "de": "de_de",
    "el": "el_gr",
    "en": "default",  # All en_X variants use "default"
    "es": "es_es",  # es_ar, es_es, es_mx all map to es_es
    "fr": "fr_fr",
    "hu": "hu_hu",
    "id": "id_id",
    "it": "it_it",
    "ja": "ja_jp",
    "ko": "ko_kr",
    "pl": "pl_pl",
    "pt": "pt_br",
    "ro": "ro_ro",
    "ru": "ru_ru",
    "th": "th_th",
    "tr": "tr_tr",
    "vi": "vi_vn",
    "zh": "zh_cn",  # zh_cn, zh_my, zh_tw all map to zh_cn
}

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "resources" / "skinid_mapping"


def fetch_json(url: str, timeout: int = 30) -> Optional[Dict]:
    """Fetch JSON data from URL with error handling."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] Failed to fetch {url}: {e}")
        return None


def fetch_champion_ids_from_directory(lang_code: str) -> List[int]:
    """Fetch list of champion IDs from the champions directory listing for a specific language."""
    # URL-encode the language code
    encoded_lang = lang_code.replace("_", "%5F")
    url = f"{CDRAGON_BASE_URL}/{encoded_lang}/v1/champions/"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        html_content = response.text
        
        # Extract all .json filenames using regex
        json_files = re.findall(r'[">](\d+)\.json[<"]', html_content)
        
        # Convert to integers and filter
        champion_ids = []
        for id_str in json_files:
            champion_id = int(id_str)
            # Skip -1 and very high IDs (test champions like Doom Bots)
            if champion_id > 0 and champion_id < 10000:
                champion_ids.append(champion_id)
        
        # Remove duplicates and sort
        champion_ids = sorted(set(champion_ids))
        return champion_ids
        
    except Exception as e:
        print(f"  [ERROR] Failed to fetch champion directory for {lang_code}: {e}")
        return []


def parse_champion_skins_and_chromas(champion_data: Dict) -> List[Dict]:
    """Parse skins and chromas from champion JSON data."""
    skins_list = []
    
    # Get skins array from champion data
    skins = champion_data.get('skins', [])
    
    for skin in skins:
        if not isinstance(skin, dict):
            continue
        
        skin_id = skin.get('id', 0)
        skin_name = skin.get('name', 'Unknown')
        
        # Add the main skin
        skin_entry = {
            'id': str(skin_id),
            'name': skin_name
        }
        skins_list.append(skin_entry)
        
        # Prestige skins don't have chromas, skip chroma processing for them
        if 'Prestige' in skin_name or 'prestige' in skin_name.lower():
            continue
        
        # Add chromas as separate skin entries
        chromas = skin.get('chromas', [])
        for chroma in chromas:
            chroma_id = chroma.get('id', 0)
            chroma_name = chroma.get('name', 'Unknown Chroma')
            
            chroma_entry = {
                'id': str(chroma_id),
                'name': chroma_name
            }
            skins_list.append(chroma_entry)
    
    return skins_list


def build_skin_ids_for_language(locale: str) -> bool:
    """Build skin_ids.json for a specific language."""
    print(f"\n{'='*70}")
    print(f"Processing locale: {locale}")
    print(f"{'='*70}")
    
    # Extract language code from locale (ll from ll_ll)
    # All en_X variants and "default" map to "en"
    if locale == "default":
        lang_code = "en"
    else:
        lang_code = locale.split("_")[0] if "_" in locale else locale
    
    # URL-encode the locale for API calls
    encoded_lang = locale.replace("_", "%5F")
    
    # Create output directory using language code (ll), not locale (ll_ll)
    lang_output_dir = OUTPUT_DIR / lang_code
    lang_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Fetch champion IDs using the locale (for API calls)
    print(f"Fetching champion IDs...")
    champion_ids = fetch_champion_ids_from_directory(locale)
    
    if not champion_ids:
        print(f"[ERROR] No champion IDs found for {lang_code}")
        return False
    
    print(f"Found {len(champion_ids)} champions")
    
    # Dictionary to store all skin mappings
    skin_mapping = {}
    
    # Counter for statistics
    total_champions = 0
    total_skins = 0
    failed_champions = []
    
    # Process each champion
    print(f"\nProcessing champions...")
    for champion_id in champion_ids:
        try:
            # Fetch champion data
            url = f"{CDRAGON_BASE_URL}/{encoded_lang}/v1/champions/{champion_id}.json"
            champion_data = fetch_json(url)
            
            if not champion_data:
                failed_champions.append(champion_id)
                continue
            
            # Extract champion name
            champion_name = champion_data.get('name', f'Champion_{champion_id}')
            
            # Parse skins and chromas
            skin_data = parse_champion_skins_and_chromas(champion_data)
            
            if not skin_data:
                print(f"  [WARNING] {champion_name:<20} No skins found")
                continue
            
            # Add to mapping
            for skin in skin_data:
                skin_id = skin.get('id')
                skin_name = skin.get('name')
                
                if skin_id and skin_name:
                    skin_mapping[skin_id] = skin_name
            
            total_champions += 1
            total_skins += len(skin_data)
            print(f"  [OK] {champion_name:<20} {len(skin_data):>3} skins")
            
        except Exception as e:
            print(f"  [ERROR] Processing champion ID {champion_id}: {e}")
            failed_champions.append(champion_id)
            continue
    
    # Save the skin mapping to JSON file
    output_file = lang_output_dir / "skin_ids.json"
    print(f"\nWriting skin mappings to: {output_file}")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(skin_mapping, f, indent=2, ensure_ascii=False)
        
        print(f"\n[SUCCESS] {lang_code}")
        print(f"  - Total champions: {total_champions}")
        print(f"  - Total skins: {total_skins}")
        print(f"  - Failed champions: {len(failed_champions)}")
        if failed_champions:
            print(f"  - Failed IDs: {failed_champions[:10]}{'...' if len(failed_champions) > 10 else ''}")
        print(f"  - Output file: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Writing output file for {lang_code}: {e}")
        return False


def main():
    """Main function to build skin_ids.json for all languages."""
    print("="*70)
    print("Building Multi-Language Skin IDs Mapping")
    print("="*70)
    print("Note: All variants of the same language use the same mapping")
    print("      Files are saved using language codes (ll) instead of locales (ll_ll)")
    print("="*70)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    successful_langs = []
    failed_langs = []
    processed_lang_codes = set()  # Track which language codes we've already processed
    
    # Process each locale, but only once per language code
    for locale in LANGUAGES:
        # Extract language code from locale (ll from ll_ll)
        if locale == "default":
            lang_code = "en"
        else:
            lang_code = locale.split("_")[0] if "_" in locale else locale
        
        # Skip if we've already processed this language code
        if lang_code in processed_lang_codes:
            print(f"\n[Skipping] {locale} -> {lang_code} (already processed)")
            continue
        
        try:
            success = build_skin_ids_for_language(locale)
            if success:
                successful_langs.append(f"{locale} -> {lang_code}")
                processed_lang_codes.add(lang_code)
            else:
                failed_langs.append(f"{locale} -> {lang_code}")
        except Exception as e:
            print(f"\n[ERROR] Fatal error processing {locale}: {e}")
            failed_langs.append(f"{locale} -> {lang_code}")
    
    # Summary
    print("\n" + "="*70)
    print("Processing Complete!")
    print("="*70)
    print(f"Successfully processed: {len(successful_langs)} unique language codes")
    print(f"Failed languages: {len(failed_langs)}")
    
    if successful_langs:
        print(f"\nSuccessful languages:")
        for lang in successful_langs:
            print(f"  - {lang}")
    
    if failed_langs:
        print(f"\nFailed languages:")
        for lang in failed_langs:
            print(f"  - {lang}")
    
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print("="*70)


if __name__ == "__main__":
    main()


