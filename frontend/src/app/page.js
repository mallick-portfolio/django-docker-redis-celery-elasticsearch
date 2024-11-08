"use client";
import React, { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import axios from "axios";
const Home = () => {
  const [searchInput, setSearchInput] = useState("");
  const getSearch = async (searchInput) => {
    const response = await axios.get(
      `http://localhost:8000/api/v1/posts/search/mother/`
    );
    const result = await response.data;
    return result;
  };

  useEffect(() => {
    const data = getSearch(searchInput);
    console.log(data);
  }, [searchInput]);

  console.log(searchInput);
  return (
    <div className="flex w-screen items-center justify-center h-screen">
      <div>
        <Input
          type="search"
          placeholder="Search..."
          onChange={(e) => setSearchInput(e.target.value)}
        />
      </div>
    </div>
  );
};

export default Home;
