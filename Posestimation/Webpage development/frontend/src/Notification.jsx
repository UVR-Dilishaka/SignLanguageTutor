import { forwardRef } from "react";

const Notification = forwardRef((props, ref) => {
    return <>
        <div ref={ref} className="notification-box">
        </div>
    </>
});

export default Notification;
