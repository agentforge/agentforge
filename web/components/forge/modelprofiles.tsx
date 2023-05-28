import React, { useEffect, useState } from 'react';
import 'tailwindcss/tailwind.css';
import MenuButton from '@/components/shared/menubutton';

interface ModelProfile {
  avatar: string;
  name: string;
  creator: string;
  description: string;
  timestamp: string;
}

const API_ENDPOINT = '/api/modelprofiles'; // replace with your actual endpoint
const ModelProfilesTable: React.FC<{pageSize: number}> = ({pageSize}) => {
  const [profiles, setProfiles] = useState<ModelProfile[]>([]);
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    const fetchProfiles = async () => {
      try {
          const user_id = "test_user";
          const res = await fetch(`/api/modelprofiles/${user_id}`);
          const data = await res.json();
          setProfiles(data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchProfiles();
  }, []);

  const profilesToShow = profiles.slice((currentPage-1)*pageSize, currentPage*pageSize);

  return (
    <>
    <div className='dark flex w-1/4'>
    <MenuButton route="/forge/config/editor">
      New
    </MenuButton>
    </div>   
    <div className="dark bg-gray-800 text-white">
      <table className="table-auto w-full">
        <thead>
          <tr>
            <th className="px-4 py-2">Avatar</th>
            <th className="px-4 py-2">Name</th>
            <th className="px-4 py-2">Creator</th>
            <th className="px-4 py-2">Description</th>
            <th className="px-4 py-2">Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {profilesToShow.map((profile, index) => (
            <tr key={index} className={`${index % 2 === 0 ? 'bg-gray-700' : ''}`}>
              <td className="border px-4 py-2"><img src={profile.avatar} alt="avatar" /></td>
              <td className="border px-4 py-2">{profile.name}</td>
              <td className="border px-4 py-2">{profile.creator}</td>
              <td className="border px-4 py-2">{profile.description}</td>
              <td className="border px-4 py-2">{profile.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="py-4">
        {Array(Math.ceil(profiles.length / pageSize)).fill(0).map((_, index) => (
          <button
            key={index}
            className={`mx-1 p-2 rounded ${currentPage === index+1 ? 'bg-blue-500' : 'bg-gray-700'}`}
            onClick={() => setCurrentPage(index+1)}
          >
            {index+1}
          </button>
        ))}
      </div>
    </div>
    </>
  );
};

export default ModelProfilesTable;
