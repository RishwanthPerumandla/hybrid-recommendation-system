// src/pages/UserDetail.jsx
import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Button,
  Tabs,
  Tab,
  CircularProgress,
  Pagination,
} from "@mui/material";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import PostGrid from "../components/PostGrid";

const UserDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const user = location.state;

  const [tabIndex, setTabIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [posts, setPosts] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPosts, setTotalPosts] = useState(0);
  const pageSize = 6;

  const tabApis = [
    `/likes/${id}`,
    `/recommend/content?user_id=${id}`,
    `/recommend/collab?user_id=${id}`,
    `/recommend/hybrid?user_id=${id}`,
  ];

  const tabLabels = ["Liked Posts", "Content-Based", "Collaborative", "Hybrid"];

  const loadPosts = async () => {
    setLoading(true);
    try {
      const skip = (page - 1) * pageSize;
      const apiWithParams =
        tabIndex === 0
          ? `${tabApis[tabIndex]}?skip=${skip}&limit=${pageSize}`
          : `${tabApis[tabIndex]}&skip=${skip}&limit=${pageSize}`;

      const res = await axios.get(`http://localhost:8000${apiWithParams}`);
      const key = tabIndex === 0 ? "liked_posts" : "recommendations";
      setPosts(res.data[key] || []);
      setTotalPosts(res.data.pagination?.total || res.data.returned || 0);
    } catch (err) {
      console.error("Error fetching posts:", err);
      setPosts([]);
    }
    setLoading(false);
  };

  useEffect(() => {
    setPage(1); // Reset page when switching tabs
  }, [tabIndex]);

  useEffect(() => {
    loadPosts();
  }, [tabIndex, page]);

  const handlePageChange = (_, value) => setPage(value);

  if (!user) {
    return (
      <Box p={3}>
        <Typography variant="h6">User not found. Please go back.</Typography>
        <Button variant="contained" onClick={() => navigate("/")}>
          Back to Users
        </Button>
      </Box>
    );
  }

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        👤 {user.name} ({user.email})
      </Typography>
      <Button variant="outlined" onClick={() => navigate("/")}>
        ⬅️ Back to Users
      </Button>

      <Tabs
        value={tabIndex}
        onChange={(e, newIndex) => setTabIndex(newIndex)}
        sx={{ my: 2 }}
        variant="scrollable"
        scrollButtons="auto"
      >
        {tabLabels.map((label, idx) => (
          <Tab label={label} key={idx} />
        ))}
      </Tabs>

      {loading ? (
        <Box mt={4} display="flex" justifyContent="center">
          <CircularProgress />
        </Box>
      ) : (
        <>
          <PostGrid posts={posts} />
          {totalPosts > pageSize && (
            <Box mt={4} display="flex" justifyContent="center">
              <Pagination
                count={Math.ceil(totalPosts / pageSize)}
                page={page}
                onChange={handlePageChange}
                color="primary"
              />
            </Box>
          )}
        </>
      )}
    </Box>
  );
};

export default UserDetail;
