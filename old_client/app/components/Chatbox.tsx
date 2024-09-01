import React, { useContext, useEffect, useRef } from "react";
import SessionContext from "../context/session";
import moment from "moment";
import {
    BotMessage,
    ChatboxContainer,
    ChatTimeIndicator,
    HumanMessage,
    SessionStateIndicator,
  } from "./Chatbox-style";


const Chatbox = () => {
  const messageElement = useRef<HTMLDivElement>(null);
  const { messages, socketState } = useContext(SessionContext);

  useEffect(() => {
    if (null !== messageElement.current) {
      messageElement.current.addEventListener(
        "DOMNodeInserted",
        (event: any) => {
          const { currentTarget: target } = event;
          target.scroll({ top: target.scrollHeight, behavior: "smooth" });
        }
      );
    }
  }, [messages]);

  return (
    <>
      <SessionStateIndicator state={socketState}></SessionStateIndicator>
      <ChatboxContainer ref={messageElement}>
        {messages?.map((message, index) =>
          message?.msg.substring(0, 5) === "Human" ? (
            <HumanMessage key={message.id}>
              <p>{message.msg}</p>
              <ChatTimeIndicator>
                {moment(message.timestamp, "YYYYMMDD").fromNow()}
              </ChatTimeIndicator>
            </HumanMessage>
          ) : (
            <BotMessage key={message.id}>
              <p>{message.msg}</p>
              <ChatTimeIndicator>
                {" "}
                {moment(message.timestamp, "YYYYMMDD").fromNow()}
              </ChatTimeIndicator>
            </BotMessage>
          )
        )}
      </ChatboxContainer>
    </>
  );
};

export default Chatbox;