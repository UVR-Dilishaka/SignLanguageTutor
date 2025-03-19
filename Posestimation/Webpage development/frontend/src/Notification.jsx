import { forwardRef } from "react";

const Notification = forwardRef((props, ref) => {
    return <>
        <div ref={ref} className="notification-box">
            <div className="close-notification">Ok</div>
        </div>
    </>
});

export default Notification;
