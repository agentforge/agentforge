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
  persona: persona;
}

interface persona {
  // Define properties related to the avatar configuration
  name: string;
  display_name: string;
}

const API_ENDPOINT = '/api/modelprofiles'; // replace with your actual endpoint

const ModelProfilesTable: React.FC<{ pageSize: number }> = ({ pageSize }) => {
  const router = useRouter();
  const [profiles, setProfiles] = useState<ModelProfile[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date());


  // Custom Hook for handling client-side navigation
  function useLinkHandler() {
    let router = useRouter();

    useEffect(() => {
      let onClick = e => {
        let link = e.target.closest('a');
        if (
          link &&
          link instanceof HTMLAnchorElement &&
          link.href &&
          (!link.target || link.target === '_self') &&
          link.origin === location.origin &&
          !link.hasAttribute('download') &&
          e.button === 0 && // left clicks only
          !e.metaKey && // open in new tab (mac)
          !e.ctrlKey && // open in new tab (windows)
          !e.altKey && // download
          !e.shiftKey &&
          !e.defaultPrevented
        ) {
          e.preventDefault();
          router.push(link.href);
        }
      };
    })
  };

  useEffect(() => {
    const fetchProfiles = async () => {
      try {
        const user_id = "test_user";
        const res = await fetch(`/api/user/${user_id}/modelprofiles`);
        const data = await res.json();
        setProfiles(data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchProfiles();
  }, [lastUpdated]);

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
      setLastUpdated(new Date());
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
      setLastUpdated(new Date());
    } catch (err) {
      console.error(err);
    }
  };

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
            <th className="px-4 py-2">ID</th>
            <th className="px-4 py-2"></th>  
          </tr>
        </thead>
        <tbody>
          {profilesToShow.map((profile, index) => (
            <tr key={index} className={`${index % 2 === 0 ? 'bg-gray-700' : ''}`}>
              <td className="border px-4 py-2"><img src={profile.avatar} alt="avatar" /></td>
              <td className="border px-4 py-2">{profile.persona.name}</td>
              <td className="border px-4 py-2">{profile.persona.display_name}</td>
              <td className="border px-4 py-2">
                <Button type='button' onClick={() => handleDelete(profile._id)} extraClasses="float-right">
                  <TrashIcon />
                </Button>
                <a href={`/forge/chat/${profile._id}`} role="button" aria-label="Edit">
                  <div className="cursor-pointer inline-block w-[48px] bg-transparent hover:bg-slate-500 text-slate-100 font-semibold hover:text-white py-2 px-4 border border-slate-100 hover:border-transparent rounded">
                    <PlayIcon/>
                  </div>
                </a>
                {/* <Button type='button' onClick={() => gotoProfile(profile._id)}>
                  <PlayIcon/>
                </Button> */}
                <a href={`/forge/config/edit/${profile._id}`} role="button" aria-label="Edit">
                  <div className="cursor-pointer inline-block w-[48px] bg-transparent hover:bg-slate-500 text-slate-100 font-semibold hover:text-white py-2 px-4 border border-slate-100 hover:border-transparent rounded">
                      <Pencil1Icon />
                  </div>
                </a>
                <Button type='button' onClick={() => handleCopy(profile._id)} extraClasses="float-left">
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
