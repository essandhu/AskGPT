import React from 'react';

interface MessageProps {
  sender: 'human' | 'bot';
  text: string;
}

const Message: React.FC<MessageProps> = ({ sender, text }) => {
  const isBot = sender === 'bot';
  const messageClass = isBot ? 'bg-blue-500 text-white' : 'bg-gray-300 text-black';
  
  return (
    <div className={`p-3 rounded-lg mb-2 max-w-xs ${messageClass} ${isBot ? 'self-start' : 'self-end'}`}>
      {text}
    </div>
  );
};

export default Message;
