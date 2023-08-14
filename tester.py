import PIL.Image
import PIL.ImageDraw


def draw_transparent_rectangle(image, top_left, bottom_right, color, transparency):
    """Draws a rectangle on the given image with the specified transparency.

    Args:
      image: The image to draw the rectangle on.
      top_left: The top-left corner of the rectangle.
      bottom_right: The bottom-right corner of the rectangle.
      color: The color of the rectangle.
      transparency: The transparency of the rectangle, from 0 to 255.

    Returns:
      The image with the rectangle drawn on it.
    """

    # Create a new image the same size as the original image, initialized to fully
    # transparent black.

    # Create a drawing context for the new image.
    draw = PIL.ImageDraw.Draw(image)

    # Draw the rectangle on the new image.
    draw.rectangle(top_left + bottom_right, fill=color + (transparency,))

    # Alpha composite the new image with the original image.
    return


if __name__ == "__main__":
    # Load the image.
    image = PIL.Image.open("resources/general/back_fire.jpg").convert("RGBA")

    # Draw a transparent rectangle on the image.
    new_image = draw_transparent_rectangle(
        image, (10, 10), (100, 100), (255, 0, 0), 128
    )

    # Save the new image.
    new_image.save("new_image.png")
