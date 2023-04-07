import { useCallback, useState, useEffect } from 'react';

export function useStateWithCallback<T>(
  initialValue: T,
  callback: (value: T) => void
): [T, React.Dispatch<React.SetStateAction<T>>] {
  const [state, setState] = useState<T>(initialValue);

  useEffect(() => {
    callback(state);
  }, [state, callback]);

  return [state, setState];
}

export default useStateWithCallback;