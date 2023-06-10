import React, { useRef, useState, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid'; // make sure to install uuid library

interface ReflectionProps {
  id: string;
  type: string;
  text: string;
}

const Reflection: React.FC = () => {
  const thoughtHistoryRef = useRef<HTMLUListElement>(null);

  const [reflections, setReflections] = useState<ReflectionProps[]>([]);

  const addReflection = useCallback(async (text: string, type: string) => {
    if (!text) {
      console.log('ERROR: Must set text.');
      return;
    }

    if (!type) {
      console.log('ERROR: Must set type.');
      return;
    }

    const newReflection: ReflectionProps = {
      id: uuidv4(),
      type,
      text,
    };

    setReflections((prevReflections) => [...prevReflections, newReflection]);
  }, []);

  return (
    <div className="md:block md:w-2/12">
      <div className="mx-auto">
        <ul
          ref={thoughtHistoryRef}
          className="thought-history"
          style={{ maxHeight: '500px', overflow: 'scroll', fontSize: '10px' }}
        >
          {reflections.map((reflection) => (
            <li key={reflection.id}>
              <b>{reflection.type}: </b> {reflection.text}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Reflection;
