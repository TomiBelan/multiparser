function hello(values, n)
    my_string = [[5]]
    <?py
        my_nested_array = [[5]]
        if len(values) > 5:
            print("over 5 values")
            # ?> this is in a comment so it doesn't count
        else: yield n
        %lua{
            print("back" .. " in " .. "lua")
        }
        assert True
    ?>
    result = %calc(5 + %py(10 ** 6) * 6)
end
