# LoL Skins

League of Legends skin assets organized by champion and skin IDs.

## Structure

```
skins/
├── {champion_id}/
│   ├── {skin_id}/
│   │   ├── {skin_id}.png
│   │   ├── {skin_id}.zip
│   │   └── {chroma_id}/
│   │       ├── {chroma_id}.png
│   │       └── {chroma_id}.zip
│   └── {skin_id}/
│       ├── {skin_id}.zip
│       └── {chroma_id}/
│           ├── {chroma_id}.png
│           └── {chroma_id}.zip
```

**Notes:**
- Each skin has its own directory named with the skin ID
- Some skins have both PNG and ZIP files, others only have ZIP files
- Chromas are stored in subdirectories within their parent skin directory
- Champion IDs are numeric (e.g., 1, 10, 101, etc.)
- Skin IDs are typically 6-digit numbers (e.g., 100000, 100001, etc.)
- Chroma IDs are typically 6-digit numbers (e.g., 100010, 100011, etc.)

## Discord

Join our community: [League Unlocked](https://discord.gg/zUhnk7Ac)

## License

Open source. Please respect Riot Games' intellectual property rights.
