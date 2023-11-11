import { Alert, AlertTitle } from '@mui/material';
import React, { useCallback, useEffect, useState } from 'react';

const NotificationPanel = ({}) => {
  const [message, setMessage] = useState(null);
  useEffect(() => {
    const eventSource = new EventSource('http://localhost:5001/events');
    eventSource.addEventListener('publish', function (event) {
      var data = JSON.parse(event.data);
      setMessage({
        ...data.message,
        time:
          new Date().toLocaleDateString() +
          ' ' +
          new Date().toLocaleTimeString(),
      });
    });
    return () => eventSource.close();
  }, []);

  useEffect(() => {
    if (message) {
      const timeout = setTimeout(() => setMessage(null), 10000);
      return () => clearTimeout(timeout);
    }
  }, [message]);

  const onCloseHandler = useCallback(() => {
    setMessage(null);
  }, []);

  if (!message) return <></>;

  return (
    <Alert
      style={{
        position: 'absolute',
        top: '1rem',
        right: '1rem',
        zIndex: 10,
      }}
      severity="info"
      onClose={onCloseHandler}
    >
      <AlertTitle>Server notification: {message.title}</AlertTitle>
      {message.message}
      <br />
      {message.time}
    </Alert>
  );
};

export default NotificationPanel;
