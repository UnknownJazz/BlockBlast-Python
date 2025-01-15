from PIL import Image, ImageDraw

class ImageCreator:
    def generateMatrix(self, width, height, matrix, save_as):
        # Define the color map
        color = {
            -1: "black",
            1: "purple",
            2: "blue",
            3: "yellow",
            4: "red",
            5: "green"
        }

        # Create a new blank image
        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)

        # Determine the size of each square
        rows = len(matrix)
        cols = len(matrix[0])
        square_width = width // cols
        square_height = height // rows

        # Draw the matrix on the image
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                # Get the top-left and bottom-right corners of the square
                top_left = (j * square_width, i * square_height)
                bottom_right = ((j + 1) * square_width, (i + 1) * square_height)
                
                # Get the color for the current value
                square_color = color.get(value, "white")  # Default to white if value not in color dict
                
                # Draw the square
                draw.rectangle([top_left, bottom_right], fill=square_color)

        # Save the image
        img.save(f"{save_as}.png")
        print(f"Image saved as {save_as}.png")
