import React, { useState, useEffect } from 'react';
import AddSchedule from './AddSchedule';
import AddSchedule2 from './AddSchedule2';
import AddSchedule3 from './AddSchedule3';
import styled from 'styled-components';

const Container = styled.div`
  .overlaps-form-container {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .overlaps-form {
    width: 50%;
  }

  h2 {
    font-size: 24px;
    margin-bottom: 20px;
    color: #333;
  }

  .form-group {
    margin-bottom: 20px;
  }

  p {
    font-size: 18px;
    margin-bottom: 10px;
  }

  .schedule-container {
    margin-top: 20px;
  }

  button {
    background-color: #134f28;
    color: #fff;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-right: 10px;
  }

  button:hover {
    background-color: #1a8041;
  }

  .schedule-form {
    margin-top: 20px;
  }

  .schedule-form.open {
    display: flex;
    align-items: end;
  }

  .schedule-form:not(.open) {
    display: none;
  }

  .schedule-form .form-container {
    background-color: #e0e0e0;
    padding: 20px;
    border-radius: 8px;
    margin-top: 10px;
    display: flex;
  }

  .form-container label {
    font-size: 16px;
    color: #333;
  }

  .form-container select,
  .form-container input[type='time'],
  .form-container input[type='number'] {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-top: 5px;
    margin-bottom: 10px;
  }

  .button-group {
    margin-top: 20px;
  }

  .button-group button {
    background-color: #134f28;
    color: #fff;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-right: 10px;
  }

  .button-group button:hover {
    background-color: #1a8041;
  }
`;

const StepTwo = ({ setTotal }) => {
  const [showArray, setShowArray] = useState(false);
  const [showOnPremises, setShowOnPremises] = useState(false);
  const [showCloudStore, setShowCloudStore] = useState(false);
  const [arraySchedules, setArraySchedules] = useState([]);
  const [onPremisesSchedules, setOnPremisesSchedules] = useState([]);
  const [cloudStoreSchedules, setCloudStoreSchedules] = useState([]);
  const [count_snap, setCount_snap] = useState(0);
  const [count_onprim, setCount_onprim] = useState(0);
  const [count_cloud, setCount_cloud] = useState(0);





  useEffect(() => {
    setTotal(prevTotal => ({
      ...prevTotal,
      arraySchedules,
      onPremisesSchedules,
      cloudStoreSchedules
    }));
  }, [arraySchedules, onPremisesSchedules, cloudStoreSchedules, setTotal]);

  const handleSave = (data, storeType) => {

    const formattedData = data;
    switch (storeType) {
      case 'array':
        setArraySchedules([...arraySchedules, formattedData]);
        break;
      case 'onPremises':
        setOnPremisesSchedules([...onPremisesSchedules, formattedData]);
        break;
      case 'cloudStore':
        setCloudStoreSchedules([...cloudStoreSchedules, formattedData]);
        break;
      default:
        break;
    }

    setShowArray(false); // Hide the form after saving
    setShowOnPremises(false);
    setShowCloudStore(false);
  };

  const handleCancel = () => {
    setShowArray(false); // Hide the form on cancel
    setShowOnPremises(false);
    setShowCloudStore(false);
  };

  const handleAddArraySchedule1 = () => {
    setCount_snap(prevCount => prevCount + 1); // Increment count
    setShowArray(true);
  };
  const handleAddArraySchedule2 = () => {
    setCount_onprim(prevCount => prevCount + 1); // Increment count
    setShowOnPremises(true);
  };
  const handleAddArraySchedule3 = () => {
    setCount_cloud(prevCount => prevCount + 1); // Increment count
    setShowCloudStore(true);
  };

  return (
    <Container>
      <div className="overlaps-form-container">
        <div className="overlaps-form">
          <h2>Add Protection Policy</h2>
          <div className="form-group">
            <p>HPE Array Volumes</p>

            <div className="schedule-container">
              <h2>Array Snapshots</h2>
              <button onClick={handleAddArraySchedule1}>+ Add Schedule</button>

              {showArray && (
                <AddSchedule count={count_snap + count_onprim + count_cloud} onSave={(data) => handleSave(data, 'array')} onCancel={handleCancel} />

              )}

              {arraySchedules.length > 0 && (
                <div>
                  <p>All Array Schedules:</p>
                  {arraySchedules.map((schedule, index) => (
                    <p key={index}>
                      {`Every ${schedule.backupFrequency.value} ${schedule.backupFrequency.unit
                        } , Start-After: ${schedule.StartAfter} , Retain For: ${schedule.retainFor.value
                        } ${schedule.retainFor.unit}`}
                    </p>
                  ))}
                </div>
              )}

              <h2>On-Premises Protection Store</h2>
              <button onClick={handleAddArraySchedule2}>+ Add Schedule</button>

              {showOnPremises && (
                <AddSchedule2 count={count_snap + count_onprim + count_cloud} onSave={(data) => handleSave(data, 'onPremises')} onCancel={handleCancel} count_onprim={count_snap} />
              )}
              {onPremisesSchedules.length > 0 && (
                <div>
                  <p>All On-Premises Schedules:</p>
                  {onPremisesSchedules.map((schedule, index) => (
                    <p key={index}>
                      {`Every ${schedule.backupFrequency.value} ${schedule.backupFrequency.unit
                        } , Start-After: ${schedule.StartAfter} , Retain For: ${schedule.retainFor.value
                        } ${schedule.retainFor.unit}`}
                    </p>
                  ))}
                </div>
              )}

              <h2>HPE Cloud Store</h2>
              <button onClick={handleAddArraySchedule3}>+ Add Schedule</button>

              {showCloudStore && (
                <AddSchedule3 count={count_snap + count_onprim + count_cloud} onSave={(data) => handleSave(data, 'cloudStore')} onCancel={handleCancel} count_cloud={count_onprim - count_snap} count_snap={count_snap} />
              )}
              {cloudStoreSchedules.length > 0 && (
                <div>
                  <p>All Cloud Store Schedules:</p>
                  {cloudStoreSchedules.map((schedule, index) => (
                    <p key={index}>
                      {`Every ${schedule.backupFrequency.value} ${schedule.backupFrequency.unit
                        } , Start-After ${schedule.StartAfter} , Retain For: ${schedule.retainFor.value
                        } ${schedule.retainFor.unit}`}
                    </p>
                  ))}
                </div>
              )}

              <div className="schedule-form" id="scheduleForm"></div>
            </div>
          </div>
        </div>
      </div>
    </Container>
  );
};

export default StepTwo;
