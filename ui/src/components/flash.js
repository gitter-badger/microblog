import { useState, useEffect } from 'preact/hooks';

import Bus from '../utils/Bus';

const Flash = () => {
  const [visibility, setVisibitiy] = useState(false);
  const [message, setMessage] = useState('');
  const [type, setType] = useState('');

  useEffect(() => {
    Bus.addListener('flash', ({ message, type }) => {
      setVisibitiy(true);
      setMessage(message);
      setType(type);
      setTimeout(() => {
        setVisibitiy(false);
      }, 4000);
    });
  });

  useEffect(() => {
    const el = document.querySelector('.flash-close');
    if (el !== null) {
      el.addEventListener('click', () => setVisibitiy(false));
    }
  });

  return (
    visibility &&
    <div class={`toast toast-${type}`}>
      <button class="btn btn-clear float-right flash-close" />
      {message}
    </div>
  );
};

export default Flash;
