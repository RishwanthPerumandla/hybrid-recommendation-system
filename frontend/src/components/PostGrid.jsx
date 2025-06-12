// src/components/PostGrid.jsx
import React, { useState } from "react";
import {
  Grid,
  Card,
  CardMedia,
  CardContent,
  Typography,
  Pagination,
  Box,
} from "@mui/material";

const PostGrid = ({ posts, pageSize = 6 }) => {
  const [page, setPage] = useState(1);

  const handlePageChange = (event, value) => {
    setPage(value);
  };

  const paginatedPosts = posts.slice((page - 1) * pageSize, page * pageSize);
  const pageCount = Math.ceil(posts.length / pageSize);

  if (!posts?.length) {
    return <Typography>No posts available.</Typography>;
  }

  return (
    <Box>
      <Grid container spacing={3}>
        {paginatedPosts.map((post) => (
          <Grid item xs={12} sm={6} md={4} key={post._id}>
            <Card>
              {post.image && (
                <CardMedia
                  component="img"
                  height="180"
                  image={post.image}
                  alt={post.title}
                />
              )}
              <CardContent>
                <Typography variant="h6">{post.title}</Typography>
                <Typography variant="body2" color="text.secondary">
                  Category: {post.category}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Type: {post.post_type}
                </Typography>
                {post.similarity_score && (
                  <Typography variant="caption">
                    Similarity: {post.similarity_score}
                  </Typography>
                )}
                {post.matched_reason && (
                  <Typography variant="caption">
                    <br />💡 {post.matched_reason}
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {pageCount > 1 && (
        <Box display="flex" justifyContent="center" mt={4}>
          <Pagination
            count={pageCount}
            page={page}
            onChange={handlePageChange}
            color="primary"
          />
        </Box>
      )}
    </Box>
  );
};

export default PostGrid;
