"use client";
import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { axios } from "../middleware/axios";
import SessionContext from "../context/session";

const Home = () => {
  const { setToken, name, setName, setSessionStart } =
    useContext(SessionContext);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  console.log(name);

  const handleInput = (event: any) => {
    setName(event.target.value);
  };

  const CREATE_SESSION = async () => {
    try {
      setLoading(true);
      const token = await axios.post(`/token?name=${name}`);
      setToken(token?.data.token);
      setName(token?.data.name);
      setSessionStart(token?.data.session_start);
      setLoading(false);
      navigate(`chat/${token.data.token}`);
    } catch (error: any) {
      setLoading(false);
      if (error?.message === "timeout exceeded") {
        setError("An unknown error has occured, Please try again later");
      } else if (error?.response.status === 400) {
        setError("Error! Provide Required Credentials");
      } else {
        setError("An unknown error has occured, Please try again later");
      }
    }
  };

  const onSubmit = (event: any) => {
    event.preventDefault();
    if (name.length > 0) {
      CREATE_SESSION();
    } else {
      setError("Error! Provide Required Credentials");
    }
  };

  return (
    <div>
      <h1>AskGPT</h1>
      <p>AskGPT is a chatbot</p>

      {loading ? (
        <div>
          <p>Loading session...</p>
        </div>
      ) : (
        <form onSubmit={onSubmit}>
          <input
            placeholder="Enter your name to start chat"
            value={name}
            type="text"
            onChange={handleInput}
          ></input>
          <button type="submit">Start Chat</button>
        </form>
      )}
    </div>
  );
};

export default Home;
