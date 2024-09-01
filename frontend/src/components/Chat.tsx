import React, { useState, useEffect, useRef } from 'react';
import { v4 as uuid4 } from 'uuid';
import Message from './Message';

interface MessageData {
  sender: 'human' | 'bot';
  text: string;
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<MessageData[]>([]);
  const [input, setInput] = useState<string>('');
  const [isPaused, setPause] = useState<boolean>(false);
  const ws = useRef<WebSocket | null>(null);
  const token = useRef<string>(uuid4()); // Generate a new token for each session

  useEffect(() => {
    // Create WebSocket connection on component mount
    ws.current = new WebSocket(`ws://127.0.0.1:3500/chat?token=${token.current}`);

    ws.current.onopen = () => {
      console.log("WebSocket connection established");
    };

    ws.current.onclose = () => {
      console.log("WebSocket connection closed");
    };

    ws.current.onerror = (error) => {
      console.error("WebSocket error: ", error);
    };

    ws.current.onmessage = (event: MessageEvent) => {
      if (isPaused) return;

      // Debug incoming message
      console.log("Message received:", event.data);

      const message = event.data;
      setMessages(prevMessages => [...prevMessages, { sender: 'bot', text: message }]);
    };

    return () => {
      ws.current?.close();
    };
  }, [isPaused]);

  const updateMessages = (event: React.FormEvent) => {
    event.preventDefault();
    if (input.length > 0) {
      const chat: MessageData = {
        sender: 'human',
        text: input,
      };
      setMessages(prevMessages => [...prevMessages, chat]);

      // Send the message to the WebSocket server
      ws.current?.send(input);
      setInput("");
    }
  };

  return (
    <div className="flex flex-col items-center p-4 h-screen bg-gray-100">
      <div className="flex flex-col w-full max-w-lg h-full overflow-y-auto">
        {messages.map((msg, index) => (
          <Message key={index} sender={msg.sender} text={msg.text} />
        ))}
      </div>
      <form onSubmit={updateMessages} className="flex w-full max-w-lg mt-4">
        <input
          type="text"
          className="flex-grow p-2 border border-gray-400 rounded-l-lg"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && updateMessages(e)}
        />
        <button
          type="submit"
          className="p-2 bg-blue-500 text-white rounded-r-lg"
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default Chat;
