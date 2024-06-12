import React from 'react';
import { useState, useEffect } from 'react';
import './styles.css'; // Import CSS file for styles

// Example data
const categories = [
    { id: 1, name: "SNAPSHOT" },
    { id: 2, name: "BACKUP" },
    { id: 3, name: "CLOUD_BACKUP" },
    { id: 4, name: "SNAPSHOT" },
    { id: 5, name: "BACKUP" },
    { id: 6, name: "CLOUD_BACKUP" },
];

const occurrences = [
    {
        "current_id": 1,
        "current_time": "2024-04-08 02:00",
        "source_id": "None",
        "source_time": "None"
    },
    {
        "current_id": 2,
        "current_time": "2024-04-08 05:00",
        "source_id": 1,
        "source_time": "2024-04-08 02:00"
    },
    {
        "current_id": 1,
        "current_time": "2024-04-08 06:00",
        "source_id": "None",
        "source_time": "None"
    },
    {
        "current_id": 3,
        "current_time": "2024-04-08 06:00",
        "source_id": 2,
        "source_time": "2024-04-08 05:00"
    },
    {
        "current_id": 1,
        "current_time": "2024-04-08 10:00",
        "source_id": "None",
        "source_time": "None"
    },
    {
        "current_id": 1,
        "current_time": "2024-04-08 14:00",
        "source_id": "None",
        "source_time": "None"
    },
    {
        "current_id": 2,
        "current_time": "2024-04-08 17:00",
        "source_id": 1,
        "source_time": "2024-04-08 14:00"
    },
    {
        "current_id": 1,
        "current_time": "2024-04-08 18:00",
        "source_id": "None",
        "source_time": "None"
    },
    {
        "current_id": 1,
        "current_time": "2024-04-08 22:00",
        "source_id": "None",
        "source_time": "None"
    },
    {
        "current_id": 1,
        "current_time": "2024-04-09 02:00",
        "source_id": "None",
        "source_time": "None"
    },
    {
        "current_id": 2,
        "current_time": "2024-04-09 05:00",
        "source_id": 1,
        "source_time": "2024-04-09 02:00"
    },
    {
        "current_id": 1,
        "current_time": "2024-04-09 06:00",
        "source_id": "None",
        "source_time": "None"
    },
    {
        "current_id": 3,
        "current_time": "2024-04-09 06:00",
        "source_id": 2,
        "source_time": "2024-04-09 05:00"
    }
];

const timeIntervals = [...new Set(occurrences.map(occurrence => occurrence.current_time))].map(time => ({
    startTime: time
}));


// Grid component
function Grid({ categories, timeIntervals, occurrences }) {
    const [tooltipContent, setTooltipContent] = useState(null);
    const [currentSchedule, setCurrentSchedule] = useState(null);

    const handleMouseEnter = (currentId, currentTime, sourceId, sourceTime) => {
        const scheduleInfo = `Schedule ID: ${currentId}, Time: ${currentTime}`;
        const sourceInfo = sourceId === 'None' ? 'None' : `Source ID: ${sourceId}, Source Time: ${sourceTime}`;
        setTooltipContent(`${scheduleInfo}, ${sourceInfo}`);
        setCurrentSchedule({ currentId, currentTime, sourceId, sourceTime });
    };

    const handleMouseLeave = () => {
        setTooltipContent(null);
        setCurrentSchedule(null);
    };

    return (
        <div className="grid">
            <div className="grid-row">
                <div className="grid-cell header"></div>
                <div className="grid-cell header">IDs</div>
                {timeIntervals.map((interval, index) => (
                    <div key={index} className="grid-cell header time">
                        {interval.startTime}
                    </div>
                ))}
            </div>

            {categories.map(category => {
                if (category.name !== "SNAPSHOT" && category.name !== "BACKUP" && category.name !== "CLOUD_BACKUP") {
                    return null; // Skip categories other than SNAPSHOT, BACKUP, and CLOUD_BACKUP
                }
                return (
                    <div key={category.id} className="grid-row">
                        <div className="grid-cell header">{category.name}</div>
                        <div className="grid-cell header">{category.id}</div> {/* Displaying the schedule ID */}
                        {timeIntervals.map(timeInterval => {
                            const occurrencesInCell = occurrences.filter(occurrence =>
                                occurrence.current_id === category.id &&
                                occurrence.current_time.includes(timeInterval.startTime)
                            );
                            return (
                                <div
                                    key={timeInterval.startTime}
                                    className="grid-cell"
                                    onMouseEnter={() => handleMouseEnter(category.id, timeInterval.startTime)}
                                    onMouseLeave={handleMouseLeave}
                                >
                                    {occurrencesInCell.map((occurrence, index) => (
                                        <div
                                            key={index}
                                            className="circle"
                                            onMouseEnter={() => handleMouseEnter(occurrence.current_id, occurrence.current_time, occurrence.source_id, occurrence.source_time)}
                                            onMouseLeave={handleMouseLeave}
                                        >
                                            <svg width="20" height="20">
                                                <circle cx="10" cy="10" r="5" fill={occurrence.current_id === currentSchedule?.sourceId ? 'black' : 'blue'} />
                                            </svg>
                                        </div>
                                    ))}


                                </div>
                            );
                        })}
                    </div>
                );
            })}
            {/* Tooltip */}
            {tooltipContent && <div className="tooltip">{tooltipContent}</div>}
            {/* Hovering schedule info */}
            {currentSchedule && (
                <div className="hover-info">
                    <h3 className='heading'>SCHEDULE DETAILS</h3>
                    <div>Schedule ID: {currentSchedule?.currentId}</div>
                    <div>Schedule Time: {currentSchedule?.currentTime}</div>
                    <div>Source Schedule ID: {currentSchedule?.sourceId}</div>
                    <div>Source Schedule Time: {currentSchedule?.sourceTime}</div>
                </div>
            )}
        </div>
    );
}




function BackupScheduleVisualization(data) {
    // console.log("Inside Scatter Chart")
    // // console.log(data)
    // const response = data
    // console.log(response)
    // console.log(typeof (response))
    // const occurrences = response.data.map(entry => entry.occurrences).flat();

    // const categories = response.data.reduce((acc, curr) => {
    //     const schedules = curr.schedules_involved.map(schedule => ({
    //         id: schedule.id,
    //         name: schedule.type
    //     }));
    //     schedules.forEach(schedule => {
    //         if (!acc.some(category => category.id === schedule.id)) {
    //             acc.push(schedule);
    //         }
    //     });
    //     return acc;
    // }, []);
    // const timeIntervals = [...new Set(occurrences.map(occurrence => occurrence.time))].map(time => ({
    //     startTime: time
    // }));
    console.log("Occurrences:", occurrences);
    console.log("Categories:", categories);
    console.log("Timestamps", timeIntervals)
    return (
        <div className="visualization">
            <h2>Backup Schedule Visualization</h2>
            <Grid categories={categories} timeIntervals={timeIntervals} occurrences={occurrences} />
        </div>
    );
}

export default BackupScheduleVisualization;