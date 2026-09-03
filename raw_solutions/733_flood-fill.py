class Solution:
    def floodFill(self, image, sr, sc, color):
        start = image[sr][sc]
        if start == color:
            return image
        rows, cols = len(image), len(image[0])

        def dfs(r, c):
            if 0 <= r < rows and 0 <= c < cols and image[r][c] == start:
                image[r][c] = color
                dfs(r + 1, c); dfs(r - 1, c)
                dfs(r, c + 1); dfs(r, c - 1)

        dfs(sr, sc)
        return image
