// src/pages/UserList.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Pagination,
  CircularProgress,
  Stack,
  Divider,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

const UserList = () => {
  const [users, setUsers] = useState([]);
  const [totalCount, setTotalCount] = useState(0); // optional if backend returns total
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const usersPerPage = 6;
  const navigate = useNavigate();

  const fetchUsers = async (page) => {
    setLoading(true);
    try {
      const skip = (page - 1) * usersPerPage;
      const response = await axios.get(
        `http://localhost:8000/users?skip=${skip}&limit=${usersPerPage}`
      );
      setUsers(response.data.users || []);
      setTotalCount(response.data.pagination?.total || 100); // fallback if total not returned
    } catch (error) {
      console.error('❌ Failed to fetch users:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers(page);
  }, [page]);

  const handlePageChange = (_, value) => {
    setPage(value);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={10}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box p={4}>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        📋 Posts Recommendations System
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Click on a user to view their liked posts and personalized recommendations.
      </Typography>
      <Divider sx={{ mb: 3 }} />

      <Grid container spacing={3}>
        {users.map((user) => (
          <Grid item xs={12} sm={6} md={4} key={user.id}>
            <Card elevation={3} sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {user.name}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {user.email}
                </Typography>
                <Button
                  variant="contained"
                  fullWidth
                  onClick={() => navigate(`/user/${user.id}`, { state: user })}
                >
                  View Recommendations
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Stack mt={5} alignItems="center">
        <Pagination
          count={Math.ceil(totalCount / usersPerPage)} // fallback if `total` not returned
          page={page}
          onChange={handlePageChange}
          color="primary"
        />
      </Stack>
    </Box>
  );
};

export default UserList;
