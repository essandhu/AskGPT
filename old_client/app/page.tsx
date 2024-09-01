"use client";
import React, { Fragment } from "react";
import { Route, Routes } from "react-router-dom";
import Chat from "./pages/Chat";
import HomePage from "./pages/HomePage";

export default function Home() {
  return (
    <Fragment>
      <Routes>
        <Route path="/" element={<HomePage />}></Route>
        <Route path="/chat/:token_id" element={<Chat />}></Route>
      </Routes>
    </Fragment>
  );
}
