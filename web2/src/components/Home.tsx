import ControlPanel from './ControlPanel';
import Agent from './Agent';
import Gutter from './Gutter';

interface HomeProps {}

const Home: React.FC<HomeProps> = () => {

  // TODO: make dynamic, temporary until we can source these from the API
  const avatars = ["default", "makhno", "fdr"];
  const modelConfigs = ["creative", "logical", "moderate"];
  const models = ["alpaca-lora-7b"];

  return (
    <div>
      <div className="row">
        <div className="col-2 main-control">
          <ControlPanel avatars={avatars} modelConfigs={modelConfigs} models={models} />
        </div>
        <div className="col-8 interaction">
          <Agent />
        </div>
        <div className='col-2 secondary-control'>
          <Gutter/>
        </div>
      </div>
    </div>
  );
};

export default Home;
