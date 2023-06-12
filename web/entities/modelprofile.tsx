// ModelProfileContext.tsx

import React, { createContext, useContext, useState } from 'react';

// Define the Model Profile interface
interface ModelProfile {
  id: string;
  name: string;
  // Add additional properties as needed
}

// Define the context shape
interface ModelProfileContextValue {
  modelProfiles: ModelProfile[];
  fetchModelProfiles: () => Promise<void>;
  addModelProfile: (modelProfile: ModelProfile) => Promise<void>;
  updateModelProfile: (modelProfile: ModelProfile) => Promise<void>;
  deleteModelProfile: (id: string) => Promise<void>;
}

// Create the Model Profile context
const ModelProfileContext = createContext<ModelProfileContextValue | undefined>(undefined);

// Define a custom hook to access the Model Profile context
const useModelProfileContext = (): ModelProfileContextValue => {
  const context = useContext(ModelProfileContext);
  if (!context) {
    throw new Error('useModelProfileContext must be used within a ModelProfileContextProvider');
  }
  return context;
};

// Define the Model Profile context provider component
const ModelProfileContextProvider: React.FC = ({ children }) => {
  const [modelProfiles, setModelProfiles] = useState<ModelProfile[]>([]);

  const fetchModelProfiles = async () => {
    try {
      // Make an API request or fetch the model profiles from a data source
      const modelProfilesData: ModelProfile[] = await fetchModelProfilesFromAPI();
      setModelProfiles(modelProfilesData);
    } catch (error) {
      // Handle error
    }
  };

  const addModelProfile = async (modelProfile: ModelProfile) => {
    try {
      // Make an API request or add the model profile to a data source
      const addedModelProfile: ModelProfile = await addModelProfileToAPI(modelProfile);
      setModelProfiles((prevModelProfiles) => [...prevModelProfiles, addedModelProfile]);
    } catch (error) {
      // Handle error
    }
  };

  const updateModelProfile = async (modelProfile: ModelProfile) => {
    try {
      // Make an API request or update the model profile in a data source
      const updatedModelProfile: ModelProfile = await updateModelProfileInAPI(modelProfile);
      setModelProfiles((prevModelProfiles) =>
        prevModelProfiles.map((mp) => (mp.id === updatedModelProfile.id ? updatedModelProfile : mp))
      );
    } catch (error) {
      // Handle error
    }
  };

  const deleteModelProfile = async (id: string) => {
    try {
      // Make an API request or delete the model profile from a data source
      await deleteModelProfileFromAPI(id);
      setModelProfiles((prevModelProfiles) => prevModelProfiles.filter((mp) => mp.id !== id));
    } catch (error) {
      // Handle error
    }
  };

  const contextValue: ModelProfileContextValue = {
    modelProfiles,
    fetchModelProfiles,
    addModelProfile,
    updateModelProfile,
    deleteModelProfile,
  };

  return (
    <ModelProfileContext.Provider value={contextValue}>{children}</ModelProfileContext.Provider>
  );
};

export { ModelProfileContextProvider, useModelProfileContext };
