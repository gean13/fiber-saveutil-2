# Persona 5 Royal PC & PS5 Save Utility

A save conversion/decryption utility for P5R PC and PS5.
(This is a fork of https://github.com/zarroboogs/fiber-saveutil, which was enhanced to also include PS5 save files)

## Requirements

- For save conversion - **decrypted** PS4 saves. Supported versions:
  - `CUSA17416` (P5R US)
  - `CUSA17419` (P5R EU)
- For PS5 save import/export - **Garlic Save Manager** (running on a jailbroken PS5).
- For save decryption - PC/PS5 saves.
- Python 3+
  - Install Python dependencies with `python -m pip install -r requirements.txt`

## Usage

### Converting PS4 Saves to PC or PS5 Saves

1. Using your preferred method, dump some **decrypted** P5R saves from your PS4 (e.g. using [Apollo Save Tool][1] or PS4 Save Mounter + ftp) or export decrypted saves using **Garlic Save Manager** on PS5.

   You should end up with a folder structure similar to:

   ```txt
   ps4_saves/CUSA17416_DATA01/DATA.DAT
   ps4_saves/CUSA17416_DATA01/sce_sys/param.sfo

   ps4_saves/CUSA17416_DATA02/DATA.DAT
   ps4_saves/CUSA17416_DATA02/sce_sys/param.sfo

   ...

   ps4_saves/CUSA17416_DATA16/DATA.DAT
   ps4_saves/CUSA17416_DATA16/sce_sys/param.sfo

   ps4_saves/CUSA17416_SYSTEM/SYSTEM.DAT
   ps4_saves/CUSA17416_SYSTEM/sce_sys/param.sfo
   ```

2. **Backup your dumped saves**, then convert the save folder using the command for your target platform:

   - **For PS5 Output (Garlic Save Manager):**
     ```txt
     python fiber-saveutil.py convert /path/to/ps4_saves/ /path/to/output_saves/ --target-platform ps5 --size 4896
     ```
     *(The `--size 4896` flag applies exact byte-padding required by Garlic Save Manager for PS5 containers).*

   - **For PC Output:**
     ```txt
     python fiber-saveutil.py convert /path/to/ps4_saves/ /path/to/output_saves/ --target-platform pc
     ```

   The result should look like the following:

   ```txt
   output_saves/DATA01/DATA.DAT
   output_saves/DATA02/DATA.DAT
   output_saves/DATA03/DATA.DAT
   output_saves/DATA04/DATA.DAT
   output_saves/DATA05/DATA.DAT
   output_saves/DATA06/DATA.DAT
   output_saves/DATA07/DATA.DAT
   output_saves/DATA08/DATA.DAT
   output_saves/DATA09/DATA.DAT
   output_saves/DATA10/DATA.DAT
   output_saves/DATA11/DATA.DAT
   output_saves/DATA12/DATA.DAT
   output_saves/DATA13/DATA.DAT
   output_saves/DATA14/DATA.DAT
   output_saves/DATA15/DATA.DAT
   output_saves/DATA16/DATA.DAT
   output_saves/SYSTEM/SYSTEM.DAT
   ```

3. **Placing Converted Saves:**
   - **PC:** Place the converted saves in the game's save folder (e.g. `%APPDATA%/Roaming/SEGA/P5R/Steam/<steam_id>/` for Steam).
   - **PS5:** Use **Garlic Save Manager** to retrieve your PS5 save slot backup, overwrite the decrypted `DATA.DAT` files with the converted output files in Garlic Save Manager on your PS5 console.

4. Boot the game and load your saves.

| PS4     | Switch  | PC      | PS5     |
|:-------:|:-------:|:-------:|:-------:|
| ![x][2] | ![x][3] | ![x][4] | ![x][4] |

#### Conversion Notes

- Only English (US/EU) PS4 saves are currently supported.

- Conversion supports targeting PC or PS5 output containers (`--target-platform ps5 --size 4896` automatically handles PS5 Garlic Save Manager target buffer allocations).

- After converting a save from PS4, you should have the following outfits in your inventory:

  ```txt
  Yumizuki High (Hero)
  Yumizuki High (Ryuji)
  Gouto Costume (Morgana)
  Ouran High (Ann)
  Yumizuki High (Yusuke)
  Ouran High (Makoto)
  Ouran High (Haru)
  Ouran High (Futaba)
  Imperial Uniform (Akechi)
  Ouran High (Kasumi)
  ```

  Equipping any one of these will result in a soft-lock since the _Raidou Kuzunoha Costume & BGM Special Set_ was cut from non-PS4 versions - you'll need to use a [mod][6] to restore them on PC.

- Loading a save that was converted from PS4 without an associated `param.sfo` file should still work, however saves will appear like this in the load menu:

  ![x][5]

### Decrypting PC & PS5 Saves

The core `dump` command syntax is identical for both PC and PS5 `DATA.DAT` files. The primary difference is specifying container padding (`--size`) when repacking PS5 files for Garlic Save Manager.

- **To decrypt a save payload (PC or PS5):**

  ```txt
  python fiber-saveutil.py dump --raw /path/to/encrypted/DATA.DAT
  ```

- **To encrypt/pack a save payload:**

  - **For PC:**
    ```txt
    python fiber-saveutil.py dump /path/to/decrypted/DATA.DAT
    ```

  - **For PS5 (Garlic Save Manager):**
    ```txt
    python fiber-saveutil.py dump /path/to/decrypted/DATA.DAT --target-platform ps5 --size 4896
    ```

- **To "resign" a decrypted save:** Simply run the encrypt command above for your platform on the edited `DATA.DAT` file to write updated checksums.

#### Decryption Notes

- Make sure to **backup your saves** before running the tool.
- Saves have checksums, so you have to "resign" them after editing.
- The game supports loading decrypted saves (as long as the save checksums and container byte sizes match expected platform requirements).

[1]: https://github.com/bucanero/apollo-ps4
[2]: https://cdn.discordapp.com/attachments/546718581572894730/1032667980275920896/ps4.png
[3]: https://cdn.discordapp.com/attachments/546718581572894730/1032668019471699989/ps4_to_nx.png
[4]: https://cdn.discordapp.com/attachments/546718581572894730/1033015655307431936/ps4_to_pc.png
[5]: https://cdn.discordapp.com/attachments/546718581572894730/1032668051721703454/ps4_to_nx_without_sfo.png
[6]: https://cdn.discordapp.com/attachments/546718581572894730/1032708752538882171/Fiber_Raidou_Restore.7z
