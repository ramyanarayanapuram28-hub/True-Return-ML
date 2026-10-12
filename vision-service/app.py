import time
import os
import csv
from datetime import datetime
from image_matching import compare_four_images


ORIGINAL_FOLDER = "vision-service/test_images/original"
RETURNED_FOLDER = "vision-service/test_images/returned"


def get_images(folder):
    valid_extensions = (".jpg", ".jpeg", ".png", ".webp")

    images = []

    for filename in os.listdir(folder):
        if filename.lower().endswith(valid_extensions):
            images.append(os.path.join(folder, filename))

    images.sort()
    return images


# Get original and returned images
original_images = get_images(ORIGINAL_FOLDER)
returned_images = get_images(RETURNED_FOLDER)


print()
print("=" * 65)
print("              TRUE-RETURN")
print("        AI VISUAL VERIFICATION")
print("=" * 65)

print()
print("Original Product Photos:")

for i, image in enumerate(original_images, 1):
    print(f"  Original {i}: {os.path.basename(image)}")


print()
print("Returned Product Photos:")

for i, image in enumerate(returned_images, 1):
    print(f"  Returned {i}: {os.path.basename(image)}")


# Validate number of images
if len(original_images) != 4:
    print()
    print("ERROR: Exactly 4 original photos are required.")
    exit()

if len(returned_images) != 4:
    print()
    print("ERROR: Exactly 4 returned photos are required.")
    exit()


print()
print("-" * 65)
print("Comparing 4 returned photos against 4 original photos...")
print("-" * 65)


# Run Module 2
comparison_start = time.perf_counter()

# Run verification and collect results
verification = compare_four_images(original_images, returned_images)

# Save verification history
history_file = os.path.join("vision-service", "verification_history.csv")
file_exists = os.path.exists(history_file)

with open(history_file, "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    if not file_exists:
        writer.writerow([
            "timestamp",
            "returned_photo",
            "best_original",
            "similarity_percent",
            "result",
            "reason"
        ])

    for item in verification["results"]:
        original_index = item["best_original_index"]

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            os.path.basename(returned_images[item["returned_index"] - 1]),
            original_index,
            item["similarity_percent"],
            item["result"],
            item["reason"]
        ])

print(f"\nVerification history saved to: {history_file}")


comparison_seconds = time.perf_counter() - comparison_start
print(f"IMAGE COMPARISON TIME: {comparison_seconds:.2f} seconds")