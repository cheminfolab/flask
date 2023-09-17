const DataRow = ({name, data, edit, text=null, unit=null, units=[]}) => {
    // data formatter
    if ((data?.constructor !== Array) && !edit) return(
        <tr>
            <td className={"py-0"}>
                <b>{name}:</b>
            </td>
            <td
                className={"py-0"} onClick={() => navigator.clipboard.writeText(data)}
                style={{cursor: 'pointer'}}
            >
                {text
                    ? text
                    : data === null || data === ""
                        ? <span>-</span>
                        : unit
                            ? <span>{data} {units.find(u => u.id === unit).symbol}</span>
                            : <span>{data}</span>
                }
            </td>
        </tr>
    )
    if (!edit) return(
        <tr>
            <td rowSpan={data.length? data.length : 1} className={"py-0"}>
                <b>{name}:</b>
            </td>
            <td className={"py-0"}>
                {!data.length
                    ? <span>-</span>
                    : data.map(
                        (item, index) =>
                            <span
                                key={index}
                                className={"p-0"} onClick={() => navigator.clipboard.writeText(item)}
                                style={{cursor: 'pointer'}}
                            >
                                {item} {unit ? units.find(u => u.id === unit).symbol : null}<br/>
                            </span>
                    )
                }
            </td>
        </tr>
    )
    return(
        <tr>
            <td rowSpan={data.length} className={"py-0"}>
                <b>{name}:</b>
            </td>
            <td className={"py-0"}>
                {data.map(item =>
                    <tr className={"p-0"}>
                        <td className={"p-0"} onClick={() => navigator.clipboard.writeText(item)}>
                            {item} {unit ? units.find(u => u.id === unit).symbol : null}
                        </td>
                    </tr>)
                }
            </td>
        </tr>
    )
}

export default DataRow