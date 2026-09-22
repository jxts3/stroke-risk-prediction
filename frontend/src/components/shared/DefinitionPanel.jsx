function DefinitionPanel({ open, text }) {
  return (
    <div
      className={`grid transition-[grid-template-rows] duration-300 ease-out ${
        open ? 'mt-2 grid-rows-[1fr]' : 'grid-rows-[0fr]'
      }`}
    >
      <p className="m-0 overflow-hidden text-xs leading-relaxed text-text-dim">{text}</p>
    </div>
  )
}

export default DefinitionPanel
