import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import axios from 'axios';
import DateTimeForm from '../components/DateTime';
import BackupCard from '../components/BackUpCard';
import CostAndSizeCard from '../components/CostSizeCard';
import PolicyTree from "../components/PolicyTree";
import ScatterChart from "../components/ScatterChart";

const Dashboard = () => {
    const [dateTime, setDateTime] = useState('');
    const [customDate, setCustomDate] = useState('');
    const [resData, setResData] = useState(null);
    const [policyName, setPolicyName] = useState('');
    // change added
    // const [policyTreeData, setPolicyTreeData] = useState([]);
    const [projectionRun, setProjectionRun] = useState([]);

    const convertToCustomFormat = (isoString) => {
        const dateObj = new Date(isoString);
        const day = String(dateObj.getDate()).padStart(2, '0');
        const month = String(dateObj.getMonth() + 1).padStart(2, '0');
        const year = String(dateObj.getFullYear()).slice(2);
        const hours = String(dateObj.getHours()).padStart(2, '0');
        const minutes = String(dateObj.getMinutes()).padStart(2, '0');
        return `${day}:${month}:${year} ${hours}:${minutes}`;
    };

    const handleDateTimeChange = (date) => {
        const isoString = date.toISOString();
        const customFormattedDateTime = convertToCustomFormat(isoString);
        setCustomDate(customFormattedDateTime);
    };

    const handlePolicyNameChange = (name) => {
        setPolicyName(name);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post('/givenTime', {
                givenTime: customDate,
                policyName: policyName
            });
            setResData(res.data);
        } catch (err) {
            console.error(err);
        }

        // try {
        //     const treeRes = await axios.post('/get_policy_tree', {
        //         policyName: policyName
        //     });
        //     setPolicyTreeData(treeRes.data)
        // } catch (err) {
        //     console.error(err)
        // }

        try {
            const tableRes = await axios.post('/get_overlaps', {
                givenTime: customDate,
                policyName: policyName
            });
            setProjectionRun(tableRes.data)
        } catch (err) {
            console.log(err)
        }
    };

    const calculateTotalCount = (data) => {
        return data ? Object.values(data).reduce((total, count) => total + count, 0) : 0;
    };

    const projectionRunColors = {
        SNAPSHOT: ['#87CEEB', '#4682B4'],
        BACKUP: ['#98FB98', '#3CB371'],
        CLOUD_BACKUP: ['#FFD700', '#FF8C00']
    };

    return (
        <>
            <Navbar />
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', padding: '20px', backgroundColor: '#f5f7fa' }}>
                <DateTimeForm dateTime={dateTime} handleDateTimeChange={handleDateTimeChange} handleSubmit={handleSubmit} policyName={policyName} handlePolicyNameChange={handlePolicyNameChange} />

                <div style={{ display: 'flex', flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-around', marginTop: '20px', width: '100%' }}>
                    <BackupCard
                        title="Array Snapshots"
                        projectionData={resData?.projectionRun.SNAPSHOT}
                        activeData={resData?.Active.SNAPSHOT}
                        projectionTotal={calculateTotalCount(resData?.projectionRun.SNAPSHOT)}
                        activeTotal={calculateTotalCount(resData?.Active.SNAPSHOT)}
                        projectionColor={projectionRunColors.SNAPSHOT[0]}
                        activeColor={projectionRunColors.SNAPSHOT[1]}
                    />

                    <BackupCard
                        title="On-Premises Backups"
                        projectionData={resData?.projectionRun.BACKUP}
                        activeData={resData?.Active.BACKUP}
                        projectionTotal={calculateTotalCount(resData?.projectionRun.BACKUP)}
                        activeTotal={calculateTotalCount(resData?.Active.BACKUP)}
                        projectionColor={projectionRunColors.BACKUP[0]}
                        activeColor={projectionRunColors.BACKUP[1]}
                    />

                    <BackupCard
                        title="Cloud Backups"
                        projectionData={resData?.projectionRun.CLOUD_BACKUP}
                        activeData={resData?.Active.CLOUD_BACKUP}
                        projectionTotal={calculateTotalCount(resData?.projectionRun.CLOUD_BACKUP)}
                        activeTotal={calculateTotalCount(resData?.Active.CLOUD_BACKUP)}
                        projectionColor={projectionRunColors.CLOUD_BACKUP[0]}
                        activeColor={projectionRunColors.CLOUD_BACKUP[1]}
                    />

                    <CostAndSizeCard
                        title="Cost and Size - Array Snapshots"
                        costAndSizeData={Object.fromEntries(Object.entries(resData?.CostAndSize || {}).filter(([key, value]) => value.type === 'SNAPSHOT'))}
                        pieChartColors={projectionRunColors.SNAPSHOT}
                    />

                    <CostAndSizeCard
                        title="Cost and Size - On-Premises Backups"
                        costAndSizeData={Object.fromEntries(Object.entries(resData?.CostAndSize || {}).filter(([key, value]) => value.type === 'BACKUP'))}
                        pieChartColors={projectionRunColors.BACKUP}
                    />

                    <CostAndSizeCard
                        title="Cost and Size - Cloud Backups"
                        costAndSizeData={Object.fromEntries(Object.entries(resData?.CostAndSize || {}).filter(([key, value]) => value.type === 'CLOUD_BACKUP'))}
                        pieChartColors={projectionRunColors.CLOUD_BACKUP}
                    />
                </div>
            </div>
            <div><PolicyTree policy={"test3"} /></div>
            <div><ScatterChart data={projectionRun} /></div>

        </>
    );
};

export default Dashboard;
