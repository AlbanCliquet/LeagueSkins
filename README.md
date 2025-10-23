# lolskins - League of Legends skin assets organized by champion and skin IDs

<div align="center">
  <img src="./icon.png" alt="League Unlocked Icon" width="128" height="128">
  
  [![Installer](https://img.shields.io/badge/Installer-Windows-blue)](https://github.com/AlbanCliquet/LeagueUnlockedReleases/releases/latest)
  [![Discord](https://img.shields.io/discord/1426680928759189545?color=5865F2&logo=discord&logoColor=white&label=Discord)](https://discord.com/invite/cDepnwVS8Z)
</div>

---

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
