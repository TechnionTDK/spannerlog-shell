CREATE FUNCTION lowercase (s text)
    RETURNS TABLE (lower text)
AS $$

yield [s.lower()]

$$ LANGUAGE plpythonu;
