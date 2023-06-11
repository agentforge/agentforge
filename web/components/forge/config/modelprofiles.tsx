import React, { useEffect, useState } from 'react';
import 'tailwindcss/tailwind.css';
import MenuButton from '@/components/shared/menubutton';
import Button from '@/components/shared/button';
import NewModelProfile from '@/components/forge/config/newprofiledialog';
import { useRouter } from 'next/navigation';
import { TrashIcon, CopyIcon, Pencil1Icon, PlayIcon } from '@radix-ui/react-icons';

interface ModelProfile {
  _id: string;
  avatar: string;
  avatar_config: avatar_config;
}

interface avatar_config {
  // Define properties related to the avatar configuration
  name: string;
}

const API_ENDPOINT = '/api/modelprofiles'; // replace with your actual endpoint

const ModelProfilesTable: React.FC<{ pageSize: number }> = ({ pageSize }) => {
  const router = useRouter();
  const [profiles, setProfiles] = useState<ModelProfile[]>([]);
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    const fetchProfiles = async () => {
      try {
        const user_id = "test_user";
        console.log(`/api/user/${user_id}/modelprofiles`);
        const res = await fetch(`/api/user/${user_id}/modelprofiles`);
        const data = await res.json();
        console.log(data);
        setProfiles(data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchProfiles();
  }, []);

  const profilesToShow = profiles.slice((currentPage - 1) * pageSize, currentPage * pageSize);
  const handleDelete = async (profileId: string) => {
    if (!profileId) {
      console.error("No profileId set!");
      return;
    }
    try {
      const response = await fetch(`/api/modelprofiles/${profileId}`, {
        method: 'DELETE',
      });
      console.log("deleteProfile", await response.json());
    } catch (err) {
      console.error(err);
    }
  }

  const handleCopy = async (profileId: string) => {
    if (!profileId) {
      console.error("No profileId set!");
      return;
    }
    try {
      const response = await fetch(`/api/modelprofiles/copy/${profileId}`, {
        method: 'POST',
      });
      console.log("copyProfile", await response.json());
    } catch (err) {
      console.error(err);
    }
  };
  
  const navToEdit = (profileId: string) => {
    router.push(`/forge/config/edit/${profileId}`);
  }
  const gotoProfile = (profileId: string) => {
    router.push(`/forge/chat/${profileId}`);
  }

  return (
    <>
    <div className='dark flex w-1/4'>
        <NewModelProfile />
    </div>   
    <div className="dark bg-gray-800 text-white">
      <table className="table-auto w-full">
        <thead>
          <tr>
            <th className="px-4 py-2">Avatar</th>
            <th className="px-4 py-2">Name</th>
            <th className="px-4 py-2">Last Edited</th>
            <th className="px-4 py-2"></th>  
          </tr>
        </thead>
        <tbody>
          {profilesToShow.map((profile, index) => (
            <tr key={index} className={`${index % 2 === 0 ? 'bg-gray-700' : ''}`}>
              <td className="border px-4 py-2"><img src={profile.avatar} alt="avatar" /></td>
              <td className="border px-4 py-2">{profile.avatar_config.name}</td>
              <td className="border px-4 py-2">
              </td>
              <td className="border px-4 py-2">
                <Button type='button' onClick={() => handleDelete(profile._id)} extraClasses="float-right">
                  <TrashIcon />
                </Button>
                <Button type='button' onClick={() => gotoProfile(profile._id)}>
                  <PlayIcon/>
                </Button>
                <Button type='button' onClick={() => navToEdit(profile._id)}>
                  <Pencil1Icon/>
                </Button>
                <Button type='button' onClick={() => handleCopy(profile._id)}>
                  <CopyIcon />
                </Button>
                </td>
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
