import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import TodoForm from "@/components/custom_ui/TodoForm";

import React from "react";

const Home = () => {
  return (
    <div className="w-screen h-screen flex justify-center items-center">
      <Card className="w-[550px] shadow-xl">
        <CardHeader>
          <CardTitle>Create New Todo</CardTitle>
        </CardHeader>
        <CardContent>
          <TodoForm />
        </CardContent>
      </Card>
    </div>
  );
};

export default Home;
