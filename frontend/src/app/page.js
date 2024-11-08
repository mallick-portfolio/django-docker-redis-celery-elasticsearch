"use client";
import React, { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import axios from "axios";
import { Card } from "@/components/ui/card";

const Home = () => {
  const [searchInput, setSearchInput] = useState("");
  const [searchData, setSearchData] = useState([]);

  const getSearchData = async (searchText) => {
    const response = await axios.get(
      `http://localhost:8000/api/v1/posts/search/${searchText}/`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    const data = await response.data;
    setSearchData(data.results);
  };

  useEffect(() => {
    if (searchInput) {
      getSearchData(searchInput);
    }
  }, [searchInput]);

  console.log(searchData);
  return (
    <div className="flex w-screen items-center justify-center h-screen">
      <div className="w-2/4">
        <Input
          type="search"
          placeholder="Search with post title ..."
          onChange={(e) => setSearchInput(e.target.value)}
        />
        {searchData.length ? (
          <Card className="p-2 mt-3">
            {searchData.map((data) => (
              <div>{data.title}</div>
            ))}
          </Card>
        ) : (
          ""
        )}
      </div>
    </div>
  );
};

export default Home;
