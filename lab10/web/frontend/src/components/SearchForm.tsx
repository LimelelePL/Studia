import { Button, Input, TextField } from "@heroui/react";

interface Props {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
}

export function SearchForm({ value, onChange, onSubmit }: Props) {
  return (
    <form
      className="flex items-end gap-2"
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit();
      }}
    >
      <TextField className="flex-1" value={value} onChange={onChange}>
        <Input className="shadow-lg" placeholder="Fragment nazwy przystanku, np. Rynek" />
      </TextField>
      <Button type="submit" variant="primary">
        Szukaj
      </Button>
    </form>
  );
}
