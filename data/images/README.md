# Industrial Equipment Image Dataset

This repository contains a small demonstration dataset used for image annotation quality assurance.

## Purpose

The images are used to demonstrate:

- Bounding box validation
- Image annotation QA
- Human annotator agreement
- IoU (Intersection over Union)
- Review queue generation
- Annotation quality scoring

## Equipment Categories

- Air Compressor
- Pump
- Valve
- Electric Motor
- Bearing
- Gearbox
- Pipiline
- Heat Exchanger
- Electrical Panel

- ## Adding Your Own Images

Replace the sample filenames with your own industrial equipment photographs.

Recommended image resolution:

- 1024×768
- 1280×720
- 1920×1080

Recommended classes:

- Air Compressor
- Pump
- Valve
- Electric Motor
- Bearing
- Gearbox
- Pipiline
- Heat Exchanger
- Electrical Panel

After adding images, update:

```
data/images.csv
```

with the corresponding filenames.

## Notes

- This dataset is intended solely for portfolio and educational purposes.
- Images remain the property of their respective copyright holders.
- No commercial redistribution is intended.

See `LICENSE_IMAGES.md` for image sources and licensing information.
