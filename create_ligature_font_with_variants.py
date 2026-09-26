import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from ligature_font import FontBuilder, FontBuildTargetSettings
from mornlight_studios_metadata import MornlightStudiosMetadataConfig


def build_single_variant_with_logging(args):
    """
    Worker function running in an isolated OS process.
    Redirects C/Python stdout and stderr to a dedicated log file per variant
    placed directly in the build output directory (relative to input_dir).
    """
    font_family, font_weight, base_font_path, svg_input_dir, build_output_dir = args

    abs_input_dir = os.path.abspath(svg_input_dir)

    # Resolve base_font_path relative to svg_input_dir matching FontBuilder's internal logic
    resolved_base_path = (
        base_font_path
        if os.path.isabs(base_font_path)
        else os.path.normpath(os.path.join(abs_input_dir, base_font_path))
    )

    # FIX: Resolve resolved_output_dir relative to svg_input_dir matching FontBuilder's internal export logic
    resolved_output_dir = (
        build_output_dir
        if os.path.isabs(build_output_dir)
        else os.path.normpath(os.path.join(abs_input_dir, build_output_dir))
    )

    # Ensure output directory exists inside resources/GameIcons/.build
    os.makedirs(resolved_output_dir, exist_ok=True)

    # Save log file directly alongside font outputs in resolved_output_dir
    log_file_path = os.path.join(resolved_output_dir, f"{font_family}-{font_weight}.log")

    if not os.path.exists(resolved_base_path):
        return font_weight, False, f"Base font file not found: {resolved_base_path}", log_file_path

    start_time = time.time()

    # Open log file and redirect stdout/stderr (including native C output from FontForge)
    with open(log_file_path, "w", encoding="utf-8") as log_file:
        # Save original file descriptors
        old_stdout_fd = os.dup(1)
        old_stderr_fd = os.dup(2)

        try:
            # Redirect stdout and stderr descriptors to log file
            os.dup2(log_file.fileno(), 1)
            os.dup2(log_file.fileno(), 2)

            # Also redirect Python sys streams
            sys.stdout = log_file
            sys.stderr = log_file

            print("==========================================")
            print(f"Building Variant: {font_family} {font_weight}")
            print(f"Base Font: {base_font_path}")
            print(f"Resolved Base Font Path: {resolved_base_path}")
            print(f"SVG Input Directory: {svg_input_dir}")
            print(f"Resolved Output Directory: {resolved_output_dir}")
            print("==========================================\n")

            font_builder = FontBuilder()
            custom_metadata = MornlightStudiosMetadataConfig() # FontMetadataConfig(copyright="", trademark="", license_url="")

            font_build_settings = FontBuildTargetSettings(
                input_dir=svg_input_dir,
                output_dir=build_output_dir,
                font_family=font_family,
                font_weight=font_weight,
                base_font_path=base_font_path,
                metadata_config=custom_metadata
            )

            font_builder.build(font_build_settings)

            elapsed = time.time() - start_time
            print(f"\nSuccessfully completed build in {elapsed:.2f}s")

            log_file.flush()
            return font_weight, True, f"Successfully built in {elapsed:.2f}s", log_file_path

        except Exception as e:
            print(f"\n❌ BUILD EXCEPTION DETECTED:\n{e}")
            log_file.flush()
            return font_weight, False, str(e), log_file_path

        finally:
            # Restore original stdout/stderr descriptors
            os.dup2(old_stdout_fd, 1)
            os.dup2(old_stderr_fd, 2)
            os.close(old_stdout_fd)
            os.close(old_stderr_fd)


if __name__ == "__main__":
    font_family = "GameIcons"
    base_font_name = "SourceSans3"
    base_font_extension = "otf"
    base_font_dir = "../source-sans-release/OTF"
    svg_input_dir = f"./resources/{font_family}"
    build_output_dir = "./.build"

    variants = [
        "Black", "BlackIt", "Bold", "BoldIt",
        "ExtraLight", "ExtraLightIt", "It", "Light",
        "LightIt", "Medium", "MediumIt", "Regular",
        "RegularIt", "Semibold", "SemiboldIt"
    ]

    tasks = []
    for font_weight in variants:
        base_font_path = f"{base_font_dir}/{base_font_name}-{font_weight}.{base_font_extension}"
        tasks.append((font_family, font_weight, base_font_path, svg_input_dir, build_output_dir))

    print(f"🚀 Starting parallel batch generation for {len(variants)} variants...")
    print(
        f"📁 Font and Log files will be saved inside: {os.path.normpath(os.path.join(svg_input_dir, build_output_dir))}\n")

    start_total_time = time.time()
    max_workers = min(os.cpu_count() or 4, len(variants))
    print(f"⚡ Spawning {max_workers} worker processes...\n")

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(build_single_variant_with_logging, task): task[1] for task in tasks}

        for future in as_completed(futures):
            variant_name = futures[future]
            try:
                weight, success, message, log_path = future.result()
                if success:
                    print(f"✅ [{weight}] {message} (Log: {os.path.basename(log_path)})")
                else:
                    print(f"❌ [{weight}] Failed: {message} (Log: {os.path.basename(log_path)})")
            except Exception as exc:
                print(f"💥 [{variant_name}] Unhandled worker exception: {exc}")

    total_time = time.time() - start_total_time
    print(f"\n🎉 Build completed in {total_time:.2f} seconds!")
