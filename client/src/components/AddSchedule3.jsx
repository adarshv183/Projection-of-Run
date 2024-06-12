import React, { useState } from 'react';


const AddSchedule3 = ({ count, onSave, onCancel, count_cloud, count_snap }) => {

    function getRandomInt(max) {
        return Math.floor(Math.random() * max + 1);
    }
    const randomCount = getRandomInt(count_cloud) + count_snap;

    const [scheduleId] = useState(count)
    const [scheduleName] = useState(`HPE_Cloud_Protection_Store_${count}`);
    const [sourceScheduleId] = useState(randomCount);

    const [backupFrequency, setBackupFrequency] = useState({ value: '', unit: 'hours' });
    const [StartAfter, setStartAfter] = useState('');

    const [retainFor, setRetainFor] = useState({ value: '', unit: 'hours' });




    const handleSave = () => {
        console.log('cloud back up Saved!');
        onSave({
            scheduleId,
            scheduleName,
            sourceScheduleId,
            backupFrequency,
            StartAfter,
            retainFor
        });
    };

    const handleCancel = () => {
        console.log('Cancelled!');
        onCancel()
    };


    const handleBackupFrequencyChange = (e) => {
        setBackupFrequency({ ...backupFrequency, value: e.target.value });
    };

    const handleBackupFrequencyUnitChange = (e) => {
        setBackupFrequency({ ...backupFrequency, unit: e.target.value });
    };

    const handleStartAfterChange = (e) => {
        setStartAfter(e.target.value);
    };



    const handleRetainForChange = (e) => {
        setRetainFor({ ...retainFor, value: e.target.value });
    };

    const handleRetainForUnitChange = (e) => {
        setRetainFor({ ...retainFor, unit: e.target.value });
    };

    return (
        <div className="form-container">

            <label htmlFor="backupFrequency">Backup Frequency:</label>
            <input type="number" id="backupFrequency" value={backupFrequency.value} onChange={handleBackupFrequencyChange} />
            <select value={backupFrequency.unit} onChange={handleBackupFrequencyUnitChange}>
                <option value="hours">Hours</option>
                <option value="days">Days</option>
                <option value="weeks">Weeks</option>
                <option value="months">Months</option>
            </select>

            <label htmlFor="timeRange">Time Range:</label>
            <input type="time" id="StartAfter" value={StartAfter} onChange={handleStartAfterChange} />


            <label htmlFor="retainFor">Retain For:</label>
            <input type="number" id="retainFor" value={retainFor.value} onChange={handleRetainForChange} />
            <select value={retainFor.unit} onChange={handleRetainForUnitChange}>
                <option value="hours">Hours</option>
                <option value="days">Days</option>
                <option value="weeks">Weeks</option>
                <option value="months">Months</option>
                <option value="years">Years</option>

            </select>

            <div className="button-group">
                <button onClick={handleCancel}>Cancel</button>
                <button onClick={handleSave}>Save</button>
            </div>

        </div>

    );
};

export default AddSchedule3;