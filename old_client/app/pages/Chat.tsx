"use client";
import React, { useContext, useEffect, useState } from "react";
import SessionContext, { MessageProps } from "../context/session";
import { axios } from "../middleware/axios";
import { useParams } from "react-router-dom";
import moment from "moment";
import Chatbox from "../components/Chatbox";
import ChatInput from "../components/ChatInput";

const Chat = () => {
  const {
    setToken,
    session_start,
    setName,
    name,
    setSessionStart,
    setMessages,
  } = useContext(SessionContext);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [chat, setChat] = useState<MessageProps>({
    id: "",
    msg: "",
    timestamp: "",
  });
  const { token_id } = useParams();

  useEffect(() => {
    const REFRESH_SESSION = async () => {
      setLoading(true);
      try {
        const token = await axios.get(`/refresh_token?token=${token_id}`);
        setToken(token?.data.token);
        setName(token?.data.name);
        setSessionStart(token?.data.session_start);
        setMessages(token?.data.messages);
        setLoading(false);
      } catch (error: any) {
        setLoading(false);
        setError("An unknown error has occured, Please try again later");
      }
    };

    REFRESH_SESSION();
  }, [token_id]);

  return (
    <div>
      <h1>Chat</h1>
      <p>Session Start: {moment(session_start, "YYYYMMDD").fromNow()}</p>
      <Chatbox />
      <ChatInput chat={chat} setChat={setChat} />
    </div>
  );
};

export default Chat;
